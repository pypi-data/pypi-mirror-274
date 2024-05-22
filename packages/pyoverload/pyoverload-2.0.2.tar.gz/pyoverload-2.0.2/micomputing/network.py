
from pycamia import info_manager

__info__ = info_manager(
    project = "PyCAMIA",
    package = "micomputing",
    author = "Yuncheng Zhou",
    create = "2022-03",
    fileinfo = "File containing U-net and convolutional networks.",
    help = "Use `from micomputing import *`.",
    requires = "batorch"
).check()

__all__ = """
    U_Net
    CNN
    FCN
    NeuralODE
""".split()
    
import math

with __info__:
    import batorch as bt
    from batorch import nn

def parse(string):
    if string.count('(') > 1 or string.count(')') > 1: raise TypeError("Invalid to parse: " + string + ". ")
    if string.count('(') == 0 and string.count(')') == 0: string += '()'
    return eval('("' + string.lower().replace('(', '", (').replace(')', ',)').replace('(,)', '()') + ')')

def cat(*tensors): return bt.cat(tensors, 1)
def combine(list_of_items, reduction):
    if len(list_of_items) >= 2:
        z = reduction(list_of_items[0], list_of_items[1])
        for i in range(2, len(list_of_items)):
            z = reduction(z, list_of_items[i])
    else: z = list_of_items[0]
    return z

class Convolution_Block(nn.Module):
    '''
    Args:
        dimension (int): The dimension of the images. 
        in_channels (int): The input channels for the block. 
        out_channels (int): The output channels for the block. 
        conv_num (int): The number of convolution layers. 
        kernel_size (int): The size of the convolution kernels. 
        padding (int): The image padding for the convolutions. 
        activation_function (class): The activation function. 
        final_activation (class): The activation function after the final convolution. 
        active_args (dict): The arguments for the activation function. 
        conv_block (str): A string with possible values in ('conv', 'dense', 'residual'), indicating which kind of block the U-Net is using: normal convolution layers, DenseBlock or ResidualBlock. 
        res_type (function): The combining type for the residual connections.
    '''
    
    def __init__(self, in_channels, out_channels, **params):
        super().__init__()
        default_values = {'dimension': 2, 'conv_num': 1, 'padding': 1, 'kernel_size': 3, 'conv_block': 'conv', 'res_type': bt.add, 'activation_function': nn.ReLU, 'final_activation': ..., 'active_args': {}}
        param_values = {}
        param_values.update(default_values)
        param_values.update(params)
        self.__dict__.update(param_values)
        self.in_channels = in_channels
        self.out_channels = out_channels
        
        if isinstance(self.padding, str): self.padding = {'SAME': self.kernel_size // 2, 'ZERO': 0, 'VALID': 0}.get(self.padding.upper(), self.kernel_size // 2)
        if self.activation_function is None: self.activation_function = lambda *a, **k: (lambda x: x)
        if self.final_activation == ...: self.final_activation = self.activation_function
        if self.final_activation is None: self.final_activation = lambda *a, **k: (lambda x: x)
        
        self.layers = nn.ModuleList()
        for i in range(self.conv_num):
            ic = self.in_channels if i == 0 else ((self.out_channels * i + self.in_channels) if self.conv_block == 'dense' else self.out_channels)
            conv = eval('nn.Conv%dd' % self.dimension)(ic, self.out_channels, self.kernel_size, 1, self.padding)
            initialize_model, initialize_params = parse(self.initializer)
            eval('nn.init.%s_' % initialize_model)(conv.weight, *initialize_params)
            if self.conv_block != 'dense': self.layers.append(conv)
            oc = (self.out_channels * i + self.in_channels) if self.conv_block == 'dense' else self.out_channels 
            self.layers.append(eval('nn.BatchNorm%dd' % self.dimension)(oc))
            if i < self.conv_num: self.layers.append(self.activation_function(**self.active_args))
            if self.conv_block == 'dense': self.layers.append(conv)

    def forward(self, x):
        if self.conv_block == 'dense':
            conv_results = [x]
            conv_layer = True
            for layer in self.layers:
                try:
                    if conv_layer: x = layer(bt.cat([bt.crop_as(l, conv_results[-1]) for l in conv_results], 1))
                    else: x = layer(x)
                except Exception as e:
                    raise e.__class__(f"In layer {layer}. " + e.__str__())
                conv_layer = layer.__class__.__name__.startswith('Conv')
                if conv_layer: conv_results.append(x)
            result = self.final_activation(**self.active_args)(x)
        else:
            y = x
            for layer in self.layers:
                try: y = layer(y)
                except Exception as e:
                    raise e.__class__(f"In layer {layer}. " + e.__str__())
            y = y.as_subclass(bt.Tensor).special_from(x)
            if self.conv_block == 'residual': z = self.res_type(bt.crop_as(x, y), y)
            else: z = y
            result = self.final_activation(**self.active_args)(z)
        result = result.as_subclass(bt.Tensor).special_from(x)
        if self.padding == self.kernel_size // 2:
            return bt.crop_as(result, x)
        return result

class U_Net(nn.Module):
    '''
    Args:
        dimension (int): The dimension of the images. Defaults to 2 (see U-Net). 
        depth (int): The depth of the U-Net. Defaults to 4 indicating 4 pooling layers and 4 up-sampling layers (see U-Net).
        conv_num (int): The number of continuous convolutions in one block. Defaults to 2. 
        padding (int or str): Indicate the type of padding used. Defaults to 'SAME' though it is 0 in conventional U-Net. 
        in_channels (int): The number of channels for the input. Defaults to 1 (see U-Net).
        out_channels (int): The number of channels for the output. Defaults to 2 (see U-Net).
        block_channels (int): The number of channels for the first block if a number is provided. Defaults to 64 (see U-Net). 
            If a list is provided, the length should be the same as the number of blocks plus two (2 * depth + 3). It represents the channels before and after each block (with the output channels included). 
            Or else, a function may be provided to compute the output channels given the block index (-1 ~ 2 * depth + 1) [including input_channels at -1 and output_channels at 2 * depth + 1]. 
        bottleneck_out_channels (int): The number of channels for the bottleneck output. Defaults to 0. 
        kernel_size (int): The size of the convolution kernels. Defaults to 3 (see U-Net). 
        pooling_size (int): The size of the pooling kernels. Defaults to 2 (see U-Net). 
        // keep_prob (float): The keep probability for the dropout layers. 
        conv_block (str): A string with possible values in ('conv', 'dense', 'residual'), indicating which kind of block the U-Net is using: normal convolution layers, DenseBlock or ResidualBlock. 
        multi_arms (str): A string with possible values in ('shared(2)', 'seperate(2)'), indicating which kind of encoder arms are used. 
        multi_arms_combine (function): The combining type for multi-arms. See skip_type for details. 
        skip_type (function): The skip type for the skip connections. Defaults to catenation (cat; see U-Net). Other possible skip types include torch.mul or torch.add. 
        res_type (function): The combining type for the residual connections. It should be torch.add in most occasions. 
        activation_function (class): The activation function used after the convolution layers. Defaults to nn.ReLU. 
        active_args (dict): The arguments for the activation function. Defaults to {}. 
        initializer (str): A string indicating the initialing strategy. Possible values are normal(0, 0.1) or uniform(-0.1, 0.1) or constant(0) (all parameters can be changed)
        with_softmax (bool): Whether a softmax layer is applied at the end of the network. Defaults to True. 
        cum_layers (list): A list consisting two numbers [n, m] indicating that the result would be a summation of the upsamples of the results of the nth to the mth (included) blocks, block_numbers are in range 0 ~ 2 * depth. 
            The negative indices are allowed to indicate the blocks in a inversed order with -1 representing the output for the last block. 
    '''
    
    class Softmax(nn.Module):
        def forward(self, x): return nn.functional.softmax(x, 1)
    
    class Encoder_Block(nn.Module):
        
        def __init__(self, in_channels, out_channels, has_pooling, params):
            super().__init__()
            block_params = params.copy()
            block_params.update({'in_channels': in_channels, 'out_channels': out_channels, 'has_pooling': has_pooling})
            self.__dict__.update(block_params)
            if has_pooling: self.pooling = eval('nn.MaxPool%dd' % self.dimension)(self.pooling_size, ceil_mode = True)
            self.conv_block = Convolution_Block(**block_params)

        def forward(self, x):
            if self.has_pooling: y = self.pooling(x)
            else: y = x
            return self.conv_block(y)
            
    class Decoder_Block(nn.Module):
        
        def __init__(self, list_of_encoders, in_channels, out_channels, params, copies_of_inputs):
            super().__init__()
            block_params = params.copy()
            block_params.update({'in_channels': in_channels, 'out_channels': out_channels})
            self.__dict__.update(block_params)
            if self.skip_type == cat: to_channels = in_channels - list_of_encoders[0].out_channels
            else: assert all([in_channels == encoder.out_channels for encoder in list_of_encoders]); to_channels = in_channels
            self.upsampling = eval('nn.ConvTranspose%dd' % self.dimension)(in_channels * copies_of_inputs, to_channels, self.pooling_size, self.pooling_size, 0)
            block_params.update({'in_channels': to_channels + sum([encoder.out_channels for encoder in list_of_encoders]), 'out_channels': out_channels})
            self.conv_block = Convolution_Block(**block_params)

        def forward(self, x, list_of_encoder_results):
            y = self.upsampling(x)
            if self.padding == self.kernel_size // 2:
                to_combine = list_of_encoder_results + [bt.crop_as(y, list_of_encoder_results[0])]
            else: to_combine = [bt.crop_as(encoder_result, y) for encoder_result in list_of_encoder_results] + [y]
            joint = combine(to_combine, self.skip_type)
            return self.conv_block(joint)


    def __init__(self, **params):
        super().__init__()
        default_values = {'dimension': 2, 'depth': 4, 'conv_num': 2, 'padding': 'SAME', 'in_channels': 1, 'out_channels': 2, 'block_channels': 64, 'kernel_size': 3, 'pooling_size': 2, 'keep_prob': 0.5, 'conv_block': 'conv', 'multi_arms': "shared", 'multi_arms_combine': cat, 'skip_type': cat, 'res_type': bt.add, 'activation_function': nn.ReLU, 'active_args': {}, 'initializer': "normal(0, 0.1)", 'with_softmax': True, 'cum_layers': -1, 'bottleneck_out_channels': 0}
        param_values = {}
        param_values.update(default_values)
        param_values.update(params)
        self.__dict__.update(param_values)
        
        if isinstance(self.block_channels, int):
            self.block_channels = [self.in_channels] + [self.block_channels << min(i, 2 * self.depth - i) for i in range(2 * self.depth + 1)] + [self.out_channels]
        bchannels = self.block_channels
        if not callable(self.block_channels): self.block_channels = lambda i: bchannels[i + 1]
        
        if isinstance(self.padding, str): self.padding = {'SAME': self.kernel_size // 2, 'ZERO': 0, 'VALID': 0}.get(self.padding.upper(), self.kernel_size // 2)
        
        if isinstance(self.cum_layers, int): self.cum_layers = [self.cum_layers, self.cum_layers]
        l, u = self.cum_layers
        l = (l + 2 * self.depth + 1) % (2 * self.depth + 1)
        u = (u + 2 * self.depth + 1) % (2 * self.depth + 1)
        if l > u: l, u = u, l
        self.cum_layers = [max(l, self.depth), min(u, 2 * self.depth)]
        
        param_values = {k: self.__dict__[k] for k in param_values}
        
        self.arm_type, self.arm_num = parse(self.multi_arms)
        self.arm_num = 1 if len(self.arm_num) == 0 else self.arm_num[0]
        if self.arm_type == 'shared': self.dif_arm_num = 1
        else: self.dif_arm_num = self.arm_num
        
        for iarm in range(self.dif_arm_num):
            for k in range(self.depth + 1):
                setattr(self, 'block%d_%d' % (k, iarm), self.Encoder_Block(self.block_channels(k - 1), self.block_channels(k), k != 0, param_values))
        
        if self.bottleneck_out_channels > 0:
            param_values = {k: v for k, v in param_values.items() if k not in ('in_channels', 'out_channels')}
            setattr(self, 'bottleneck_out', Convolution_Block(self.block_channels(self.depth) * self.arm_num, self.bottleneck_out_channels, **param_values))

        for k in range(self.cum_layers[0], self.depth + 1):
            conv = eval('nn.Conv%dd' % self.dimension)(self.block_channels(k), self.block_channels(2 * self.depth + 1), 1, 1, 0)
            initialize_model, initialize_params = parse(self.initializer)
            eval('nn.init.%s_' % initialize_model)(conv.weight, *initialize_params)
            if k < self.cum_layers[1]:
                setattr(self, 'block%dout' % k, nn.Sequential(conv, self.activation_function(**self.active_args)))
                setattr(self, 'out%dupsample' % k, eval('nn.ConvTranspose%dd' % self.dimension)(
                    self.block_channels(2 * self.depth + 1), self.block_channels(2 * self.depth + 1), self.pooling_size, self.pooling_size, 0
                ))
            else: setattr(self, 'block%dout' % k, conv)

        for k in range(self.depth + 1, self.cum_layers[1] + 1):
            setattr(self, 'block%d' % k, self.Decoder_Block(
                [getattr(self, 'block%d_%d' % (2 * self.depth - k, iarm)) for iarm in range(self.dif_arm_num)] * (self.arm_num // self.dif_arm_num), 
                self.block_channels(k - 1), self.block_channels(k), param_values, 
                self.arm_num if k == self.depth + 1 and self.multi_arms_combine == cat else 1
            ))
            conv = eval('nn.Conv%dd' % self.dimension)(self.block_channels(k), self.block_channels(2 * self.depth + 1), 1, 1, 0)
            initialize_model, initialize_params = parse(self.initializer)
            eval('nn.init.%s_' % initialize_model)(conv.weight, *initialize_params)
            if k < self.cum_layers[1]:
                setattr(self, 'block%dout' % k, nn.Sequential(conv, self.activation_function(**self.active_args)))
                setattr(self, 'out%dupsample' % k, eval('nn.ConvTranspose%dd' % self.dimension)(
                    self.block_channels(2 * self.depth + 1), self.block_channels(2 * self.depth + 1), self.pooling_size, self.pooling_size, 0
                ))
            else: setattr(self, 'block%dout' % k, conv)

        if self.with_softmax: self.softmax = self.Softmax()
        self.to(bt.get_device().main_device)
        
    @property
    def bottleneck(self):
        if self.bottleneck_out_channels > 0:
            result = getattr(self, f'block{self.depth}result', None)
            if result is None: return
            return self.bottleneck_out(result).mean(...)
        else: return

    def forward(self, x):
        size = x.size()[1:]
        if len(size) == self.dimension and self.in_channels == 1: x = x.unsqueeze(1)
        elif len(size) == self.dimension + 1 and self.in_channels * self.arm_num == size[0]: pass
        else: raise ValueError(f"The input tensor does not correspond to the U-Net structure: got {size}, but requires ([{self.in_channels * self.arm_num}], n_1, ⋯, n_{self.dimension}). ")
        
        assert size[0] % self.arm_num == 0
        inputs = x.split(size[0] // self.arm_num, 1)
        assert len(inputs) == self.arm_num
        
        for i, y in enumerate(inputs):
            for k in range(self.depth + 1):
                y = getattr(self, 'block%d_%d' % (k, 0 if self.arm_type == 'shared' else i))(y)
                setattr(self, 'block%d_%dresult' % (k, i), y)
        
        to_combine = [getattr(self, 'block%d_%dresult' % (self.depth, i)) for i in range(self.arm_num)]
        z = combine(to_combine, self.multi_arms_combine)
        setattr(self, 'block%dresult' % self.depth, z)
        
        for k in range(self.depth + 1, self.cum_layers[1] + 1):
            z = getattr(self, 'block%d' % k)(z, [getattr(self, 'block%d_%dresult' % (2 * self.depth - k, iarm)) for iarm in range(self.arm_num)])
            setattr(self, 'block%dresult' % k, z)

        t = 0
        for k in range(self.cum_layers[0], self.cum_layers[1] + 1):
            setattr(self, 'block_out%dresult' % k, getattr(self, 'block%dout' % k)(getattr(self, 'block%dresult' % k)) + t)
            if k < self.cum_layers[1]: t = getattr(self, 'out%dupsample' % k)(getattr(self, 'block_out%dresult' % k))
        
        if self.with_softmax: return self.softmax(getattr(self, 'block_out%dresult' % k))
        else: return getattr(self, 'block_out%dresult' % k)
        
    def optimizer(self, lr=0.001): return bt.Optimization(bt.optim.Adam, self.parameters(), lr)

    def loss(self, x, y):
        y_hat = self(x)
        clamped = y_hat.clamp(1e-10, 1.0)
        self.y_hat = y_hat
        return - bt.sum(y * bt.log(clamped), 1).mean().mean()
        
    def __getitem__(self, i):
        if self.arm_num == 1 and i <= self.depth: i = (i, 0)
        return getattr(self, 'block%dresult' % i if isinstance(i, int) else 'block%d_%dresult' % i)
        
    def __iter__(self):
        for i in range(2 * self.depth + 1):
            if i <= self.depth:
                for iarm in range(self.arm_num):
                    yield 'block%d_%dresult' % (i, iarm), (i, iarm)
            else: yield 'block%dresult' % i, i

class CNN(U_Net):
    '''
    Args:
        dimension (int): The dimension of the images. Defaults to 2 (see VGG). 
        blocks (int): The number of the downsampling blocks. Defaults to 5 blocks (see VGG).
        conv_num (int or list of length 'blocks'): The number of continuous convolutions in one block. Defaults to [2, 2, 3, 3, 3] (see VGG).
            If the numbers for all blocks are the same, one can use one integer.
        padding (int or str): Indicate the type of padding used. Defaults to 'SAME' indicating a same output shape as the input. 
        in_channels (int): The number of channels for the input. Defaults to 1 (see VGG).
        out_elements (int): The number of channels for the output, as the number of classification. Defaults to 1000 for 1000 classes.
        layer_channels (int or list of length 'blocks'): The number of channels for each block. Defaults to [64, 128, 256, 512, 512] (see VGG). 
            Or else, a function may be provided to compute the output channels given the block index (-1 ~ 2 * depth + 1). 
        kernel_size (int): The size of the convolution kernels. Defaults to 3 (see VGG). 
        pooling_size (int): The size of the pooling kernels. Defaults to 2 (see VGG). 
        // keep_prob (float): The keep probability for the dropout layers. 
        conv_block (str): A string with possible values in ('conv', 'dense', 'residual'), indicating which kind of block the U-Net is using: normal convolution layers, DenseBlock or ResidualBlock. 
        multi_arms (str): A string with possible values in ('shared(2)', 'seperate(2)'), indicating which kind of encoder arms are used. 
        multi_arms_combine (function): The combining type for multi-arms. Defaults to catenation (cat). Other possible skip types include torch.mul or torch.add. 
        res_type (function): The combining type for the residual connections. It should be torch.add in most occasions. 
        activation_function (class): The activation function used after the convolution layers. Defaults to nn.ReLU. 
        active_args (dict): The arguments for the activation function. Defaults to {}. 
        initializer (str): A string indicating the initialing strategy. Possible values are normal(0, 0.1) or uniform(-0.1, 0.1) or constant(0) (all parameters can be changed)
        with_softmax (bool): Whether a softmax layer is applied at the end of the network. Defaults to True. 
    '''
    
    def __init__(self, dimension = 2, blocks = 5, conv_num = 2, padding = 'SAME', 
        in_channels = 1, out_elements = 2, layer_channels = 64, kernel_size = 3, 
        pooling_size = 2, keep_prob = 0.5, conv_block = 'conv', multi_arms = "shared", 
        multi_arms_combine = cat, res_type = bt.add, activation_function = nn.ReLU,
        active_args = {}, initializer = "normal(0, 0.1)", with_softmax = True):
        depth = blocks - 1
        if isinstance(layer_channels, int):
            maxlc = layer_channels
            layer_channels = [in_channels]
            multiplier = math.pow(maxlc / in_channels, 1 / (depth + 1))
            for i in range(depth):
                layer_channels.append(int(layer_channels[-1] * multiplier))
            layer_channels.append(maxlc)
            layer_channels.extend([0] * depth)
            layer_channels.append(out_elements)
        super().__init__(dimension = dimension, depth = depth, conv_num = conv_num, 
            padding = padding, in_channels = in_channels, out_channels = out_elements, 
            block_channels = layer_channels, kernel_size = kernel_size, 
            pooling_size = pooling_size, keep_prob = keep_prob, conv_block = conv_block,
            multi_arms = multi_arms, multi_arms_combine = multi_arms_combine, skip_type = None,
            res_type = res_type, activation_function = activation_function, active_args = active_args,
            initializer = initializer, with_softmax = with_softmax, cum_layers = depth)

    def forward(self, x):
        wsm = self.with_softmax
        self.with_softmax = False
        if wsm: r = self.softmax(super().forward(x).flatten(2).mean(-1))
        else: r = super().forward(x).flatten(2).mean(-1)
        self.with_softmax = wsm
        return r
        
class FCN(nn.Module):
    '''
    Fully connected network, with hidden layers of increased and then decreased sizes. 
        For layer_elements = 64 and layers = 8 and in_elements = out_elements = 8, 
        the layer sizes are [8, 16, 32, 64, 64, 32, 16, 8]. 
    
    Args:
        layers (int): Indicate the number of fully connected layers. 
        in_elements (int): The number of elements for the input. Defaults to 1.
        out_elements (int): The number of elements for the output, as the number of classification. Defaults to 1000 for 1000 classes.
        layer_elements (int or list of length 'layers'): The number of channels for each block. In a VGG, it should be [64, 128, 256, 512, 512]. 
            Or else, a function may be provided to compute the output channels given the block index (-1 ~ 2 * depth + 1). 
        kernel_size (int): The size of the convolution kernels. Defaults to 3. 
        keep_prob (float): The keep probability for the dropout layers. 
        activation_function (class): The activation function used after the convolution layers. Defaults to nn.ReLU. 
        active_args (dict): The arguments for the activation function. Defaults to {}. 
        initializer (str): A string indicating the initialing strategy. Possible values are normal(0, 0.1) or uniform(-0.1, 0.1) or constant(0) (all parameters can be changed)
        with_softmax (bool): Whether a softmax layer is applied at the end of the network. Defaults to True. 
    '''

    class Softmax(nn.Module):
        def forward(self, x): return nn.functional.softmax(x, 1)
    def __init__(self, layers = 4, in_elements = 1, out_elements = 2, layer_elements = 64, 
        keep_prob = 0.5, activation_function = nn.ReLU, active_args = {}, 
        initializer = "normal(0, 0.1)", with_softmax = True):
        if isinstance(layer_elements, int):
            maxlc = layer_elements
            layer_elements = [in_elements]
            multiplier = bt.pow(maxlc / in_elements, 1 / (layers // 2 - 1))
            for i in range(layers // 2 - 1):
                layer_elements.append(int(layer_elements[-1] * multiplier))
            layer_elements.append(maxlc)
            if layers % 2 == 0: layer_elements.extend(layer_elements[-2::-1])
            else: layer_elements.extend(layer_elements[::-1])
            layer_elements[-1] = out_elements
        if isinstance(layer_elements, list):
            lc = layer_elements.copy()
            layer_elements = lambda i: lc[i]
        self.layers = []
        for l in range(layers):
            fcl = nn.Linear(layer_elements(l), layer_elements(l+1))
            initialize_model, initialize_params = parse(initializer)
            eval('nn.init.%s_' % initialize_model)(fcl.weight, *initialize_params)
            self.layers.append(fcl)
            if l < layers - 1:
                self.layers.append(activation_function(**active_args))
                self.layers.append(nn.Dropout(keep_prob))
            elif with_softmax:
                self.layers.append(self.Softmax())
        self.struct = nn.Sequential(*self.layers)
        self.to(bt.get_device().main_device)

    def forward(self, x):
        return self.struct(x)
    
class NeuralODE(nn.Module):
    '''
    Neural ODE structue. 
    => [dual stream: reference maps] dual_channels
    => [main stream: inputs] main_channels
    
    Args:
        dimension (int): The dimension of the images. 
        layers (int): The number accumulated layers. 
        conv_num (int): The number of continuous convolutions in each layer. Defaults to 2. 
        dual_channels (int): The number of channels for the dual stream ODE. Defaults to 0, indicating no dual network.
        main_channels (int): The number of channels for the main stream ODE. Defaults to 2.
        kernel_size (int): The size of the convolution kernels. Defaults to 3. 
        padding (int or str): Indicate the type of padding used. Defaults to 'SAME' indicating a same output shape as the input. 
        conv_block (str): A string with possible values in ('conv', 'dense', 'residual'), indicating which kind of block for the layers: normal convolution layers, DenseBlock or ResidualBlock. 
        res_type (function): The combining type for the residual connections. It should be torch.add in most occasions. 
        activation_function (class): The activation function used after the convolution layers. Defaults to nn.ReLU. 
        final_activation (class): The activation function after the final convolution. Defaults to self.activation_function. 
        active_args (dict): The arguments for the activation function. Defaults to {}. 
        initializer (str): A string indicating the initialing strategy. Possible values are normal(0, 0.1) or uniform(-0.1, 0.1) or constant(0) (all parameters can be changed)
        regularization (func): The regularization term for the delta terms. 
    '''
    
    class Softmax(nn.Module):
        def forward(self, x): return nn.functional.softmax(x, 1)
    
    def __init__(self, dimension = 2, layers = 10, conv_num = 2, kernel_size = 3, padding = 1, 
        dual_channels = 0, main_channels = 2, conv_block = 'conv', res_type = bt.add, 
        activation_function = nn.ReLU, final_activation = ..., active_args = {}, initializer = "normal(0, 0.1)", 
        shared = True, dual_ODE = True, time_channels = 1, auto_grad = False, regularization = None):
        super().__init__()
        
        if dual_channels == True: dual_channels = 64
        
        params = dict(dimension=dimension, conv_num=conv_num, kernel_size=kernel_size, padding=padding, 
            activation_function=activation_function, final_activation=final_activation, active_args=active_args, conv_block=conv_block, res_type=res_type, initializer=initializer)
        if dual_channels > 0:
            if dual_ODE:
                if shared:
                    self.dual_march_func = Convolution_Block(in_channels=dual_channels + time_channels, out_channels=dual_channels, **params)
                    self.dual_march = [self.dual_march_func] * layers
                else:
                    self.dual_march = []
                    for i in range(layers):
                        setattr(self, f'dual_march_func_{i}', Convolution_Block(in_channels=dual_channels + time_channels, out_channels=dual_channels, **params))
                        self.dual_march.append(getattr(self, f'dual_march_func_{i}'))
        if shared:
            self.main_march_func = Convolution_Block(in_channels=main_channels + dual_channels + time_channels, out_channels=main_channels, **params)
            self.main_march = [self.main_march_func] * layers
        else:
            self.main_march = []
            for i in range(layers):
                setattr(self, f'main_march_func_{i}', Convolution_Block(in_channels=main_channels + dual_channels + time_channels, out_channels=main_channels, **params))
                self.main_march.append(getattr(self, f'main_march_func_{i}'))
        self.layers = layers
        self.shared = shared
        self.dual_ODE = dual_ODE
        self.auto_grad = auto_grad
        self.dual_channels = dual_channels
        self.time_channels = time_channels
        self.regularization = regularization
    
    def time(self, i, n_channel):
        return (i / self.layers) * bt.ones(self.reference.shape.with_feature((n_channel,)), dtype=self.reference.dtype, device=self.reference.device)
    
    def integral(self, init_x, diff_func, time_inv = False):
        x = init_x
        for i in range(self.layers):
            i = self.layers - i - 1 if time_inv else i
            x = [(u - v) if time_inv else (u + v) for u, v in zip(x, diff_func(x, i))]
        return x
    
    def march(self, x, march_funcs, i):
        if self.time_channels > 0:
            t = self.time(i, n_channel=self.time_channels)
            return march_funcs[i](bt.cat(x, t, [])) / self.layers
        return march_funcs[i](x) / self.layers
    
    def forward_diff_func(self, x, i):
        if self.dual_channels > 0:
            main_x, dual_x = x
            delta_main_x = self.march(bt.cat(main_x, dual_x, []), self.main_march, i)
            if self.dual_ODE: # DSNODE
                delta_dual_x = self.march(dual_x, self.dual_march, i)
            else: delta_dual_x = bt.zeros_like(dual_x)
            return delta_main_x, delta_dual_x # SNODE / DSNODE
        return [self.march(x[0], self.main_march, i)] # UNODE
    
    def forward_func(self, init_x, dual_init_x=None):
        self.reference = init_x
        if self.dual_channels > 0:
            self.output, self.dual = self.integral([init_x, dual_init_x], self.forward_diff_func)
        else: self.output, = self.integral([init_x], self.forward_diff_func)
        return self.output
    
    def UNODE_backward_diff_func(self, x, i):
        main_x, d_main = x
        with bt.enable_grad():
            main_x = main_x.detach().requires_grad_(True)
            delta_main_x = self.march(main_x, self.main_march, i)
            if self.regularization is not None:
                self.regularization(delta_main_x).backward()
            delta_main_x.backward(d_main.detach())
        return delta_main_x.detach(), -main_x.grad
    
    def SNODE_backward_diff_func(self, x, i):
        main_x, d_main, d_dual = x
        with bt.enable_grad():
            main_x = main_x.detach().requires_grad_(True)
            dual_x = self.dual.detach().requires_grad_(True)
            delta_main_x = self.march(bt.cat(main_x, dual_x, []), self.main_march, i)
            if self.regularization is not None:
                self.regularization(delta_main_x).backward()
            delta_main_x.backward(d_main.detach())
        return delta_main_x.detach(), -main_x.grad, -dual_x.grad
    
    def DSNODE_backward_diff_func(self, x, i):
        main_x, dual_x, d_main, d_dual = x
        with bt.enable_grad():
            main_x = main_x.detach().requires_grad_(True)
            dual_x = dual_x.detach().requires_grad_(True)
            delta_main_x = self.march(bt.cat(main_x, dual_x, []), self.main_march, i)
            delta_dual_x = self.march(dual_x, self.dual_march, i)
            if self.regularization is not None:
                self.regularization(delta_main_x).backward()
            delta_dual_x.backward(d_dual.detach())
            delta_main_x.backward(d_main.detach())
        return delta_main_x.detach(), delta_dual_x.detach(), -main_x.grad, -dual_x.grad
    
    def backward(self, output_grad):
        output_grad = output_grad.as_subclass(bt.Tensor).view(self.output.shape)
        inits = []
        if self.dual_channels > 0:
            if self.dual_ODE:
                inits = [self.output, self.dual, output_grad, bt.zeros_like(self.dual)]
                ret = self.integral(inits, self.DSNODE_backward_diff_func, time_inv=True)[2:]
            else:
                inits = [self.output, output_grad, bt.zeros_like(self.dual)]
                ret = self.integral(inits, self.SNODE_backward_diff_func, time_inv=True)[1:]
        else:
            inits = [self.output, output_grad]
            ret = self.integral(inits, self.UNODE_backward_diff_func, time_inv=True)[1:]
        # for mlayer in ([self.main_march[0]] if self.shared else self.main_march):
        #     for p in mlayer.parameters(): p.grad = -p.grad
        # if self.dual_channels > 0:
        #     for mlayer in ([self.dual_march[0]] if self.shared else self.dual_march):
        #         for p in mlayer.parameters(): p.grad = -p.grad
        return ret
    
    class Autograd_Func(bt.autograd.Function):
        @staticmethod
        def forward(ctx, self, init_x, dual_init_x=None):
            ctx.self = self
            return self.forward_func(init_x, dual_init_x=dual_init_x)
        
        @staticmethod
        def backward(ctx, output_grad):
            return None, *ctx.self.backward(output_grad)
    
    def forward(self, init_x, dual_init_x=None):
        if self.auto_grad: return self.forward_func(init_x, dual_init_x=dual_init_x)
        if self.dual_channels == 0: return self.Autograd_Func.apply(self, init_x)
        return self.Autograd_Func.apply(self, init_x, dual_init_x)

if __name__ == "__main__":
#    unet = U_Net(multi_arms="seperate(3)", block_channels=16)
#    print(unet(bt.rand(10, 3, 100, 100)).size())
#    print(*[x + ' ' + str(unet[i].size()) for x, i in unet], sep='\n')
    unet = U_Net(
        dimension=3, 
        in_channels=2, 
        out_channels=3, 
        block_channels=4, 
        with_softmax=False, 
        initializer="normal(0.0, 0.9)", 
#        conv_block='dense', 
#        conv_num=4, 
#        active_args={'inplace': True}
    )
    print(unet(bt.rand(10, 2, 50, 50, 50)).size())
    print(*[x + ' ' + str(unet[i].size()) for x, i in unet], sep='\n')