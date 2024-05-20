from ..environment import torch,np
from ..core.image_utils import box_iou_xywh, get_yolo_box_xxyy




"""
1.LeNet
abstract:
        LeNet5是一个经典的卷积神经网络，由多个卷积层、池化层和全连接层组成。它通过卷积操作提取图像中的局部特征，利用池化层进行特征下采样，并通过全连接层进行分类。LeNet最初用于手写数字识别任务，并展现出了良好的性能。其结构简洁明了，为后续更复杂的神经网络结构提供了基础，对深度学习领域的发展产生了重要影响。

struct:
        卷积编码器：由两个卷积层组成;
        全连接层密集块：由三个全连接层组成。

input: 
        28*28的单通道（黑白）图像通过LeNet,in_channels×28×28。

output: 
        最后一层输出为10的Linear层，分别代表十种数字的类别数。

"""
class LeNet5(torch.nn.Module):
    def __init__(self,in_channels=3 ,num_classes=10):
        super(LeNet5, self).__init__()
        self.features = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, 6, 5, padding=2), # 输入通道数为in_channels，输出通道数为6，卷积核大小为5
            torch.nn.BatchNorm2d(6),
            torch.nn.Sigmoid(),
            torch.nn.AvgPool2d(kernel_size=2, stride=2), # 池化窗口2x2，步长2
            torch.nn.Conv2d(6, 16, 5), # 输入通道6，输出通道16，卷积核5x5
            torch.nn.BatchNorm2d(16),
            torch.nn.Sigmoid(),
            torch.nn.AvgPool2d(kernel_size=2, stride=2), # 池化窗口2x2，步长2
        )

        self.classifier = torch.nn.Sequential(
            torch.nn.Flatten(),
            torch.nn.Linear(16 * 5 * 5, 120),
            torch.nn.BatchNorm1d(120),
            torch.nn.Sigmoid(),
            torch.nn.Linear(120, 84),
            torch.nn.BatchNorm1d(84),
            torch.nn.Sigmoid(),
            torch.nn.Linear(84, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        #x = x.view(x.size(0), -1)  # 确保这里的展平操作是正确的
        x = self.classifier(x)
        return x



    def initialize_weights(self):
        for m in self.modules():
            if isinstance(m, torch.nn.Conv2d):
                torch.nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    torch.nn.init.zeros_(m.bias)
            elif isinstance(m, torch.nn.Linear):
                torch.nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    torch.nn.init.zeros_(m.bias)



"""
2.AlexNet
abstract:
        AlexNet 是 2012 年 ImageNet 竞赛的冠军模型，由 Alex Krizhevsky、Ilya Sutskever 和 Geoffrey Hinton 提出。

struct:
        模型首先包含了一个特征提取部分 self.features，该部分由几个卷积层、ReLU 激活函数和最大池化层组成。然后，通过一个自适应平均池化层 self.avgpool 将特征图的大小减小到 6x6。最后，通过三个全连接层 self.classifier 进行分类。

input: 
        输入图像的大小是 in_channelsx224x224（AlexNet 的原始输入大小）。

output: 
        num_classes 参数用于指定分类的类别数，你可以根据你的任务需求进行修改。
"""
# 定义AlexNet模型类，继承自nn.Module
class AlexNet(torch.nn.Module):
    # 初始化函数，用于设置网络层
    def __init__(self, in_channels=3, num_classes=1000):
        super(AlexNet,self).__init__()  # 调用父类nn.Module的初始化函数

        # 定义特征提取部分
        self.features = torch.nn.Sequential(
            # 第一个卷积层，输入通道3（RGB），输出通道64，卷积核大小11x11，步长4，填充2
            torch.nn.Conv2d(in_channels, 64, kernel_size=11, stride=4, padding=2),
            # ReLU激活函数，inplace=True表示直接修改原变量，节省内存
            torch.nn.ReLU(inplace=True),
            # 最大池化层，池化核大小3x3，步长2
            torch.nn.MaxPool2d(kernel_size=3, stride=2),

            # 第二个卷积层，输入通道64，输出通道192，卷积核大小5x5，填充2
            torch.nn.Conv2d(64, 192, kernel_size=5, padding=2),
            torch.nn.ReLU(inplace=True),
            torch.nn.MaxPool2d(kernel_size=3, stride=2),

            # 接下来的三个卷积层没有池化层
            torch.nn.Conv2d(192, 384, kernel_size=3, padding=1),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(384, 256, kernel_size=3, padding=1),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(256, 256, kernel_size=3, padding=1),
            torch.nn.ReLU(inplace=True),

            # 最后一个最大池化层
            torch.nn.MaxPool2d(kernel_size=3, stride=2),
        )

        # 自适应平均池化层，将特征图大小调整为6x6
        self.avgpool = torch.nn.AdaptiveAvgPool2d((6, 6))

        # 定义分类器部分
        self.classifier = torch.nn.Sequential(
            # Dropout层用于防止过拟合
            torch.nn.Dropout(),
            # 第一个全连接层，输入特征数量取决于上一个池化层的输出，输出4096
            torch.nn.Linear(256 * 6 * 6, 4096),
            torch.nn.ReLU(inplace=True),
            # 第二个Dropout层
            torch.nn.Dropout(),
            # 第二个全连接层，输出4096
            torch.nn.Linear(4096, 4096),
            torch.nn.ReLU(inplace=True),
            # 输出层，输出类别数由num_classes指定
            torch.nn.Linear(4096, num_classes),
        )


    def forward(self, x):
        # 数据通过特征提取部分
        x = self.features(x)
        # 数据通过自适应平均池化层
        x = self.avgpool(x)
        # 将数据展平为一维向量，以便输入到全连接层
        x = torch.flatten(x, 1)
        # 数据通过分类器部分
        x = self.classifier(x)
        # 返回最终分类结果
        return x


    def initialize_weights(self):
        for m in self.modules():
            if isinstance(m, torch.nn.Conv2d):
                torch.nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    torch.nn.init.zeros_(m.bias)
            elif isinstance(m, torch.nn.Linear):
                torch.nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    torch.nn.init.zeros_(m.bias)






# 3.定义一个VGG卷积块
class VGGBlock(torch.nn.Module):
    def __init__(self, in_channels, out_channels, num_convs, pool=True):
        """
        VGG块，包含多个卷积层和一个可选的最大池化层

        参数:
            in_channels (int): 输入通道数
            out_channels (int): 输出通道数（每个卷积层的输出通道数）
            num_convs (int): 卷积层的数量
            pool (bool, 可选): 是否在块后添加最大池化层。默认为True
        """
        super(VGGBlock, self).__init__()

        # 创建多个卷积层，每个卷积层后面都跟着ReLU激活函数
        layers = []
        for _ in range(num_convs):
            layers.append(torch.nn.Conv2d(in_channels if _ == 0 else out_channels, out_channels, kernel_size=3, padding=1))
            layers.append(torch.nn.ReLU(inplace=True))

            # 如果有池化层，则添加
        if pool:
            layers.append(torch.nn.MaxPool2d(kernel_size=2, stride=2))

            # 将所有层组合成一个Sequential模块
        self.conv_block = torch.nn.Sequential(*layers)

    def forward(self, x):
        """
        前向传播

        参数:
            x (torch.Tensor): 输入张量

        返回:
            torch.Tensor: 输出张量
        """
        x = self.conv_block(x)
        return x






#4.定义VGG16模型
class VGG16(torch.nn.Module):
    def __init__(self, in_channels=3, num_classes=1000):
        """
        VGG16模型

        参数:
            num_classes (int, 可选): 分类的数量。默认为1000
        """
        super(VGG16, self).__init__()

        # 定义特征提取部分
        self.features = torch.nn.Sequential(
            VGGBlock(in_channels, 64, 2, pool=True),  # block1: 64 channels, 2 conv layers, maxpool
            VGGBlock(64, 128, 2, pool=True),  # block2: 128 channels, 2 conv layers, maxpool
            VGGBlock(128, 256, 3, pool=True),  # block3: 256 channels, 3 conv layers, maxpool
            VGGBlock(256, 512, 3, pool=True),  # block4: 512 channels, 3 conv layers, maxpool
            VGGBlock(512, 512, 3, pool=True)  # block5: 512 channels, 3 conv layers, maxpool
        )

        # 定义分类器部分（全连接层）
        self.classifier = torch.nn.Sequential(
            torch.nn.Linear(512 * 7 * 7, 4096),  # fully connected layer, 4096 output neurons
            torch.nn.ReLU(True),
            torch.nn.Dropout(),
            torch.nn.Linear(4096, 4096),
            torch.nn.ReLU(True),
            torch.nn.Dropout(),
            torch.nn.Linear(4096, num_classes)  # fully connected layer, num_classes output neurons for classification
        )

        # 初始化权重
        for m in self.modules():
            if isinstance(m, torch.nn.Conv2d):
                torch.nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    torch.nn.init.constant_(m.bias, 0)
            elif isinstance(m, torch.nn.Linear):
                torch.nn.init.normal_(m.weight, 0, 0.01)
                torch.nn.init.constant_(m.bias, 0)

    def forward(self, x):
        """
        前向传播

        参数:
            x (torch.Tensor): 输入张量

        返回:
            torch.Tensor: 分类的logits
        """
        # 特征提取
        x = self.features(x)

        # 在将特征图送入全连接层之前，需要将其展平（flatten）
        # 假设输入图像的大小是3x224x224，经过5个池化层（每个池化层将尺寸减半）后，
        # 特征图的大小会变成 7x7
        x = x.view(x.size(0), -1)  # 展平操作，-1 表示让PyTorch自动计算该维度的大小

        # 送入分类器
        x = self.classifier(x)

        return x











#5.MLPConv层
class MLPConv(torch.nn.Module):
    """
    MLPConv层，包含一个1x1卷积层模拟MLP的行为
    """
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(MLPConv,self).__init__()
        # 第一个1x1卷积层，用于减少通道数
        self.conv1 = torch.nn.Conv2d(in_channels, hidden_channels, kernel_size=1, bias=True)

        # ReLU激活函数
        self.relu = torch.nn.ReLU(inplace=True)

        # 第二个1x1卷积层，用于恢复到输出通道数
        self.conv2 = torch.nn.Conv2d(hidden_channels, out_channels, kernel_size=1, bias=True)



    def forward(self, x):
        # 通过第一个1x1卷积层
        x = self.conv1(x)
        # 应用ReLU激活函数
        x = self.relu(x)
        # 通过第二个1x1卷积层
        x = self.conv2(x)
        # 应用ReLU激活函数
        x = self.relu(x)
        return x






#6.NiN块
class NiNBlock(torch.nn.Module):
    """
    NiN块，包含一个标准的卷积层和一个MLPConv层
    """
    def __init__(self, in_channels, num_channels , kernel_size=3, stride=1, padding=1):
        super(NiNBlock, self).__init__()
        # 标准的卷积层
        self.conv = torch.nn.Conv2d(in_channels, num_channels, kernel_size=kernel_size, stride=stride, padding=padding, bias=True)
        # MLPConv层
        self.mlpconv = MLPConv(num_channels, num_channels // 2, num_channels)



    def forward(self, x):
        # 通过标准的卷积层
        x = self.conv(x)
        # 通过MLPConv层
        x = self.mlpconv(x)
        return x






#7.Network in Network模型
class NiN(torch.nn.Module):
    """
    Network in Network模型
    输入图片大小为224x224
    """

    def __init__(self, in_channels=3, num_classes=10):
        super(NiN, self).__init__()
        # 初始卷积层
        self.features = torch.nn.Sequential(
            NiNBlock(in_channels, 96, kernel_size=11, stride=4, padding=0),  # 使用较大的卷积核和步长来减少空间维度
            torch.nn.MaxPool2d(kernel_size=3, stride=2),  # 最大池化层
            NiNBlock(96, 256, kernel_size=5, stride=1, padding=2),
            torch.nn.MaxPool2d(kernel_size=3, stride=2),
            NiNBlock(256, 384, kernel_size=3, stride=1, padding=1),
            torch.nn.MaxPool2d(kernel_size=3, stride=2),
            torch.nn.Dropout(p=0.5),  # 引入Dropout层防止过拟合
            NiNBlock(384, num_classes, kernel_size=3, stride=1, padding=1),
            # 使用全局平均池化替代全连接层
            torch.nn.AdaptiveAvgPool2d((1, 1)),
            torch.nn.Flatten()
        )

    def forward(self, x):
        # 通过特征提取层
        x = self.features(x)
        return x










#8.InceptionBlock块v1版本
"""
简介：Inception块v1版本，也称为Inception-v1，是GoogLeNet网络中的一个核心组成部分，由Google团队在2014年提出。Inception-v1的主要特点是使用多尺度的卷积操作来捕捉图像中不同层次的特征。为了实现这一目标，Inception-v1引入了称为“Inception模块”的基本构建块。一个典型的Inception模块由四个并行的卷积分支组成，每个分支执行不同尺度的卷积操作。这些分支的输出在通道维度上进行拼接，形成模块的最终输出。
结构：
1x1卷积分支：使用1x1的卷积核对输入进行卷积，这种卷积方式可以减少神经网络的参数量，并压缩通道数，提高计算效率。
3x3卷积分支：使用3x3的卷积核对输入进行卷积，以捕获局部特征。
5x5卷积分支：使用5x5的卷积核对输入进行卷积，以捕获更大范围的特征。但是，直接使用5x5的卷积核会导致计算量较大，因此在实际实现中，可能会使用两个3x3的卷积层来替代。
最大池化分支：使用3x3的最大池化层对输入进行下采样，然后使用1x1的卷积层来改变通道数。这个分支的目的是捕获更抽象的特征。
"""
class InceptionBlockV1(torch.nn.Module):
    def __init__(self,
                 in_channels,   # 输入到Inception块的通道数
                 ch1,           # 路径1：1x1卷积分支的输出通道数
                 ch2,           # 路径2：ch2[0]为3x3卷积分支的第一个1x1卷积的输出通道数（用于降维），ch2[1]为3x3卷积分支的3x3卷积的输出通道数
                 ch3,           # 路径3：ch3[0]为5x5卷积分支的第一个1x1卷积的输出通道数（用于降维），ch3[1]5x5卷积分支的5x5卷积的输出通道数
                 ch4):          # 最大池化分支的1x1卷积的输出通道数（用于降维后投影到同一通道数）
        super(InceptionBlockV1,self).__init__()

        # 路径1，单1x1卷积层，直接对输入进行1x1卷积
        self.brach1 = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, ch1, kernel_size=1),
            torch.nn.ReLU(inplace=True)
        )



        # 路径2，1x1卷积 -> 3x3卷积分支，先进行1x1卷积降维，再进行3x3卷积
        self.brach2 = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, ch2[0], kernel_size=1),      # 输入in_channels, 输出ch3x3red
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(ch2[0], ch2[1], kernel_size=3, padding=1), # 输入ch3x3red, 输出ch3x3
            torch.nn.ReLU(inplace=True)
        )



        # 路径3，1x1卷积 -> 5x5卷积分支
        self.brach3 = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, ch3[0], kernel_size=1),      # 输入in_channels, 输出ch5x5red
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(ch3[0], ch3[1], kernel_size=5, padding=2), # 输入ch5x5red, 输出ch5x5
            torch.nn.ReLU(inplace=True)
        )


        # 路径4，3x3最大池化 -> 1x1卷积分支，先进行3x3最大池化，然后进行1x1卷积改变通道数
        self.brach4 = torch.nn.Sequential(
            torch.nn.MaxPool2d(kernel_size=3, stride=1, padding=1),
            torch.nn.Conv2d(in_channels, ch4, kernel_size=1),
            torch.nn.ReLU(inplace=True)
        )



    def forward(self, x):
        branch1 = self.brach1(x)
        branch2 = self.brach2(x)
        branch3 = self.brach3(x)
        branch4 = self.brach4(x)

        # 拼接各分支的输出
        outputs = torch.cat((branch1, branch2, branch3, branch4), dim=1)
        return outputs











#9.GoogLeNet的复现
"""
简介：GoogLeNet的设计特点在于既有深度，又在横向上拥有“宽度”，并采用了一种名为Inception的核心子网络结构。这个网络名字中的“GoogLeNet”是对LeNet的致敬，LeNet是早期由Yann LeCun设计的卷积神经网络。
基本结构：
    Inception模块：这是GoogLeNet的核心子网络结构。Inception模块的基本组成结构有四个：1x1卷积、3x3卷积、5x5卷积和3x3最大池化。这四个操作并行进行以提取特征，然后将这四个操作的输出进行通道维度的拼接。这种设计使得网络能够捕捉不同尺度的特征。
    1x1卷积：在Inception模块中，1x1卷积起到了两个主要作用。首先，它可以在相同尺寸的感受野中叠加更多的卷积，从而提取到更丰富的特征。其次，它还可以用于降维，降低计算复杂度。当某个卷积层输入的特征数较多时，对输入先进行降维，减少特征数后再做卷积，可以显著减少计算量。
    辅助分类器：GoogLeNet在网络的不同深度处添加了两个辅助分类器。这些辅助分类器在训练过程中与主分类器一同进行优化，有助于提升整个网络的训练效果。
    全局平均池化：与传统的全连接层相比，全局平均池化能够减少网络参数，降低过拟合风险，并且具有更强的鲁棒性。
"""
class GoogLeNet(torch.nn.Module):
    def __init__(self, in_channels=3, num_classes=1000):
        super(GoogLeNet,self).__init__()


        # 第一个模块:使用64个通道、7x7卷积层。
        self.block1 = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, 64, kernel_size=7, stride=2, padding=3),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        )


        # 第二个模块:第一层卷积层是64个通道、1x1卷积层；第二个卷积层使用将通道数增加3x的3x3卷积层。
        self.block2 = torch.nn.Sequential(
            torch.nn.Conv2d(64, 64, kernel_size=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(64, 192, kernel_size=3, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        )


        # 第三个模块：串联两个Inception块。具体操作请看相关论文
        self.block3 = torch.nn.Sequential(
            InceptionBlockV1(192, 64, (96, 128), (16, 32), 32),
            InceptionBlockV1(256, 128, (128, 192), (32, 96), 64),
            torch.nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        )



        # 第四个模块：串联了5个Inception块
        self.block4 = torch.nn.Sequential(
            InceptionBlockV1( 480, 192, (96, 208), (16, 48), 64),
            InceptionBlockV1(512, 160, (112, 224), (24, 64), 64),
            InceptionBlockV1(512, 128, (128, 256), (24, 64), 64),
            InceptionBlockV1(512, 112, (114, 288), (32, 64), 64),
            InceptionBlockV1(528, 256, (160, 320), (32, 128), 128),
            torch.nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        )


        # 第五个模块： 其中每条路径通道数的分配思路和第三、第四模块中的一致，只是在具体数值上有所不同。 需要注意的是，第五模块的后面紧跟输出层，该模块同NiN一样使用全局平均汇聚层，将每个通道的高和宽变成1。 最后我们将输出变成二维数组，再接上一个输出个数为标签类别数的全连接层。
        self.block5 = torch.nn.Sequential(
            InceptionBlockV1(832, 256, (160, 320), (32, 128), 128),
            InceptionBlockV1(832, 384, (192, 384), (48,128), 128),
            torch.nn.AdaptiveAvgPool2d((1, 1)),
            torch.nn.Flatten()
        )

        self.features = torch.nn.Sequential(self.block1, self.block2, self.block3, self.block4, self.block5)

        # 分类器（全连接层）
        self.classifier = torch.nn.Linear(1024, num_classes)





    def forward(self, x):
        # 前向传播：通过特征提取层
        x = self.features(x)

        # 展平特征图，准备进行全连接层
        x = self.classifier(x)

        # 输出分类结果
        return x








"""
10.ResidualBlock的复现
简介：残差块允许网络学习残差映射，这有助于解决深度网络中的梯度消失和表示瓶颈问题。
参数:  
    - in_channels: 输入的通道数  
    - out_channels: 输出的通道数  
    - stride: 卷积的步长，默认为1  
"""
class ResidualBlock(torch.nn.Module):
    def __init__(self, in_channels, out_channels, strides=1):
        super(ResidualBlock, self).__init__()

        # 当输入输出通道数不同或者步长不为1时，需要使用一个1x1的卷积进行降维和步长调整
        # 这样可以确保主路径（shortcut）和残差路径（residual path）的输出形状一致
        self.shortcut = torch.nn.Sequential()
        if strides != 1 or in_channels != out_channels:
            self.shortcut = torch.nn.Sequential(
                torch.nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=strides),
            )

        # 残差路径包含两个3x3的卷积层，每个卷积层后都跟着一个批量归一化层和一个ReLU激活函数
        self.residual = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=strides, padding=1),
            torch.nn.BatchNorm2d(out_channels),
            torch.nn.LeakyReLU(0.1,inplace=True),
            torch.nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            torch.nn.BatchNorm2d(out_channels)
        )

        # 最后一个ReLU激活函数在残差块外部，以确保仅在残差路径有贡献时才进行非线性变换

    def forward(self, x):
        # 残差路径的输出
        residual = self.residual(x)

        # 主路径输出
        shortcut = self.shortcut(x)

        # 将残差路径和主路径的输出相加，并经过ReLU激活函数
        out = shortcut + residual
        out = torch.nn.functional.leaky_relu(out, 0.1)
        return out





"""
10.ResNet的复现
简介：ResNet最突出的特点是采用了残差学习（residual learning）的思想。这种思想通过引入残差块（Residual Block），跳过网络的某些层或部分，直接将输入传到后面的层中。残差块的设计使得模型可以学习到残差，即剩余的映射，而不仅仅是对输入的变换。通过引入残差连接，ResNet使得信息可以更容易地在网络中传播，即使网络非常深，梯度也可以通过残差连接直接传递到较浅层，从而避免了梯度消失的问题。

"""
class ResNet(torch.nn.Module):
    def __init__(self, in_channels=3, num_classes=1000):
        super(ResNet,self).__init__()

        # 第一个模块：7x7的卷积层+3x3的最大汇聚层
        self.block1 = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, 64, kernel_size=7, stride=2, padding=3),
            torch.nn.BatchNorm2d(64),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        )

        # 第二个模块~第五个模块都是有两个残差块组成
        self.block2 = torch.nn.Sequential(*self._resnet_block(64,64,2,True))
        self.block3 = torch.nn.Sequential(*self._resnet_block(64,128,2))
        self.block4 = torch.nn.Sequential(*self._resnet_block(128,256,2))
        self.block5 = torch.nn.Sequential(*self._resnet_block(256,512,2))

        #  特征提取
        self.features = torch.nn.Sequential(
            self.block1,self.block2,self.block3,self.block4,self.block5,
            torch.nn.AdaptiveAvgPool2d((1, 1)),
        )

        # 分类器
        self.classifier = torch.nn.Sequential(
            torch.nn.Flatten(),
            torch.nn.Linear(512,num_classes)
        )


    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

    # resnet块
    def _resnet_block(self, in_channels, out_channels, num_residual, fist_block=False):
        blk = []
        for i in range(num_residual):
            if i==0 and not fist_block:
                blk.append(ResidualBlock(in_channels, out_channels, strides=2))
            else:
                blk.append(ResidualBlock(out_channels, out_channels))
        return blk




"""
11.DenseBlock的复现
简介：一个稠密块由多个卷积块组成，每个卷积块使用相同数量的输出通道。前向传播中，将每个卷积块的输入与输出在通道上连接。
"""
class DenseBlock(torch.nn.Module):
    def __init__(self, in_channels, out_channels, num_convs):
        super(DenseBlock, self).__init__()
        self.net = torch.nn.ModuleList([self._conv_block(in_channels + i * out_channels, out_channels) for i in range(num_convs)])

    #批量生成规范层、激活层和卷积层
    def _conv_block(self, in_channels, num_channels):
        return torch.nn.Sequential(
            torch.nn.BatchNorm2d(in_channels),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(in_channels, num_channels, kernel_size=3, padding=1)
        )


    def forward(self, x):
        # 实现DenseBlock中将输出与输入相连
        features = [x]
        for layer in self.net:
            out = layer(torch.cat(features, dim=1))
            features.append(out)
        return torch.cat(features, dim=1) # 将所有输出连接在一起







"""
12.TransitionBlock
简述：过渡层，每一个稠密块都会增加通道数，因此使用过多会过于复杂，而过度层可以控制模型复杂度，通过1x1卷积层来减小通道数，并使用步幅为2的平均汇聚层减半高度和宽度
"""
class TransitionBlock(torch.nn.Module):
    def __init__(self, in_channels, out_channels):
        super(TransitionBlock, self).__init__()
        self.features = torch.nn.Sequential(
            torch.nn.BatchNorm2d(in_channels),torch.nn.ReLU(),
            torch.nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0), # 使用1x1卷积进行特征通道数的调整
            torch.nn.AvgPool2d(kernel_size=4, stride=2, padding=1)  # 使用平均池化进行特征尺寸的减半
        )



    def forward(self, x):
        return self.features(x)







"""
13.DenseNet
简述：使用4个稠密块，每个稠密块可以设定包含多少个卷积层，稠密块使用过度层来调整特征图的大小
"""
class DenseNet(torch.nn.Module):
    def __init__(self, in_channels=3, num_classes=1000,):
        super(DenseNet, self).__init__()
        # num_channels为当前的通道数，growth_rate增长率，num_convs_in_dense_block为四个稠密块包含的卷积层数
        self.num_channels = 64
        self.growth_rate = 32
        self.num_convs_in_dense_block = [4, 4, 4, 4]
        self.blk = []

        #第一个模块使用单卷积层和最大汇聚层
        self.block1 = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, self.num_channels, kernel_size=3, stride=2, padding=3),
            torch.nn.BatchNorm2d(self.num_channels),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2, stride=2, padding=0) # 使用最大池化进行下采样
        )




        # 使用4个稠密块，稠密块里的卷积层通道数即增长率设为32，所以每个稠密块将增加128个通道
        for i, num_convs in enumerate(self.num_convs_in_dense_block):
            # 添加一个稠密块
            self.blk.append(DenseBlock(self.num_channels, self.growth_rate, num_convs))

            # 上一个稠密块的输出通道数
            self.num_channels += self.growth_rate * num_convs

            # 在稠密块直接添加一个过度层，使通道数减半
            if i != len(self.num_convs_in_dense_block) - 1:
                self.blk.append(TransitionBlock(self.num_channels, self.num_channels // 2))
                self.num_channels = self.num_channels // 2


        self.features = torch.nn.Sequential(self.block1, *self.blk, torch.nn.BatchNorm2d(self.num_channels), torch.nn.ReLU(), torch.nn.AdaptiveAvgPool2d((1, 1)))

        self.classifier = torch.nn.Sequential(torch.nn.Flatten(), torch.nn.Linear(self.num_channels, num_classes))


    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x



'''
14.YOLOv3_104
    summary:此模型是在yolov3的版本上的改进算法，将多尺度检测中添加grid cell为104，以此增强小目标检测的性能。
'''
class YOLOv3_104(torch.nn.Module):
    def __init__(self, in_channels=3, num_classes=1000):
        super(YOLOv3_104, self).__init__()
        self.num_classes = num_classes

        '''
        DarkNet53_104
        简述：Dark53是在YOLOv3论文中提出来的，相比于上一代DarkNet网络加入了残差模块。能更好的避免梯度爆炸以及梯度消失。
            输入必须为：416x416 输出为特征图
        '''
        class DarkNet53_104(torch.nn.Module):
            def __init__(self,in_channels):
                super(DarkNet53_104, self).__init__()
                self.feature104 = torch.nn.Sequential(
                    self._DBL_block(in_channels, 32, 3, 1, 1),
                    self._DBL_block(32, 64, 3, 2, 1),
                    ResidualBlock(64, 64),
                    self._DBL_block(64, 128, 3, 2, 1),
                    *self._resnet_block(128, 128, 2, True)
                )
                self.feature52 = torch.nn.Sequential(
                    self._DBL_block(128, 256, 3, 2, 1),
                    *self._resnet_block(256, 256, 8, True)
                )
                self.feature26 = torch.nn.Sequential(
                    self._DBL_block(256, 512, 3, 2, 1),
                    *self._resnet_block(512, 512, 8, True)
                )
                self.feature13 = torch.nn.Sequential(
                    self._DBL_block(512, 1024, 3, 2, 1),
                    *self._resnet_block(1024, 1024, 4, True)
                )

            def forward(self, x):
                features104 = self.feature104(x)
                features52 = self.feature52(features104)
                features26 = self.feature26(features52)
                features13 = self.feature13(features26)
                return [features104, features52, features26, features13]

            # DBL块
            def _DBL_block(self, in_channels, out_channels, kernel_size, stride, padding):
                return torch.nn.Sequential(
                    torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding),
                    torch.nn.BatchNorm2d(out_channels),
                    torch.nn.LeakyReLU(negative_slope=0.2)
                )

            # resnet块
            def _resnet_block(self, in_channels, out_channels, num_residual, fist_block=False):
                blk = []
                for i in range(num_residual):
                    if i == 0 and not fist_block:
                        blk.append(ResidualBlock(in_channels, out_channels, strides=2))
                    else:
                        blk.append(ResidualBlock(out_channels, out_channels))
                return blk
        # 将DarkNet53_104实例化
        self.DarkNet53_104 = DarkNet53_104(in_channels)




        '''
        NeckNet_DarkNet53_104
        简述：专门为DarkNet53_104设计的颈部网络，用于FeatureExtractor进行特征提取之后实现多尺度检测部分。
        '''
        class NeckNet_DarkNet53_104(torch.nn.Module):
            def __init__(self):
                super(NeckNet_DarkNet53_104,self).__init__()
                self.output13_FE = torch.nn.Sequential(*self._FeatureExtractor_block(1024, 512, 3))
                self.output13_to_26_UpSample = self._UpSample_block(512, 256)


                self.output26_FE = torch.nn.Sequential(*self._FeatureExtractor_block(768, 256, 3))
                self.output26_to_52_UpSample = self._UpSample_block(256, 128)
                self.output26_FE_to_13_DownSample = self._DownSample_block(256, 256)


                self.output52_FE = torch.nn.Sequential(*self._FeatureExtractor_block(384, 128, 3))
                self.output52_to_104_UpSample = self._UpSample_block(128, 64)
                self.output52_FE_to_26_DowmSample = self._DownSample_block(128, 128)
                self.output52_FE_26_to_13_DowmSample = self._DownSample_block(128, 128)






            # FE模块设计，实现Neck网络中的特征提取部分的功能
            def _FeatureExtractor_block(self,in_channels, out_channels, num_inception):
                blk = []
                blk.append(self._DBL_block(in_channels, out_channels , 1, 1, 0))
                for i in range(num_inception):
                    blk.append(InceptionBlockV1(out_channels, ch1=(out_channels - 3 * out_channels// 4), ch2=(out_channels//4, out_channels//4), ch3=( out_channels//4, out_channels//4) , ch4=out_channels//4))
                blk.append(self._DBL_block(out_channels, out_channels , 3, 1, 1))
                return blk

            # UpSample模块，上采样模块设计。
            def _UpSample_block(self, in_channels, out_channels):
                return torch.nn.Sequential(self._DBL_block(in_channels, out_channels, 3, 1,1),
                                           torch.nn.ConvTranspose2d(out_channels, out_channels, 2, 2, 0))

            def _DownSample_block(self, in_channels, out_channels):
                return self._DBL_block(in_channels, out_channels, 3, 2,1)

            # DBL模块设计
            def _DBL_block(self, in_channels, out_channels, kernel_size, stride, padding):
                return torch.nn.Sequential(
                    torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding),
                    torch.nn.BatchNorm2d(out_channels),
                    torch.nn.LeakyReLU(negative_slope=0.2)
                )

            def forward(self, features):
                features104, features52, features26, features13 = features
                features13_FE = self.output13_FE(features13)
                features13_to_26_UpSample = self.output13_to_26_UpSample(features13_FE)


                features26_FE = self.output26_FE(torch.cat((features26, features13_to_26_UpSample), dim=1))
                features26_to_52_UpSample = self.output26_to_52_UpSample(features26_FE)


                features52_FE = self.output52_FE(torch.cat((features52, features26_to_52_UpSample), dim=1))
                features52_to_104_UpSample = self.output52_to_104_UpSample(features52_FE)

                output104 = torch.cat((features104, features52_to_104_UpSample), dim=1)

                features52_to_26_DowmSample = self.output52_FE_to_26_DowmSample(features52_FE)
                output26 = torch.cat((features26_FE, features52_to_26_DowmSample), dim=1)

                features52_to_13_DownSample = self.output52_FE_26_to_13_DowmSample(features52_to_26_DowmSample)
                features26_to_13_DownSample = self.output26_FE_to_13_DownSample(features26_FE)
                output13 = torch.cat((features13_FE, features26_to_13_DownSample, features52_to_13_DownSample), dim=1)

                return [output104, output26, output13]


        # 实例化颈部网络
        self.NeckNet_DarkNet53_104 = NeckNet_DarkNet53_104()

        self.classifier_DarkNet53_104 = torch.nn.Sequential(
            self._DBL_block(192, 3*(5+num_classes), 1, 1, 0),
            torch.nn.Conv2d(3*(5+num_classes), 3*(5+num_classes), 1, 1, 0)
        )

        self.classifier_DarkNet53_26 = torch.nn.Sequential(
            self._DBL_block(384, 3*(5+num_classes), 1, 1, 0),
            torch.nn.Conv2d(3*(5+num_classes), 3*(5+num_classes), 1, 1, 0)
        )

        self.classifier_DarkNet53_13 = torch.nn.Sequential(
            self._DBL_block(896, 3*(5+num_classes), 1, 1, 0),
            torch.nn.Conv2d(3*(5+num_classes), 3*(5+num_classes), 1, 1, 0)
        )





    def forward(self, x):
        x = self.DarkNet53_104(x)
        x = self.NeckNet_DarkNet53_104(x)
        output104, output26, output13 = x
        output104 = self.classifier_DarkNet53_104(output104)

        output26 = self.classifier_DarkNet53_26(output26)

        output13 = self.classifier_DarkNet53_13(output13)

        return [output104, output26, output13]



    # DBL模块设计
    def _DBL_block(self, in_channels, out_channels, kernel_size, stride, padding):
        return torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding),
            torch.nn.BatchNorm2d(out_channels),
            torch.nn.LeakyReLU(negative_slope=0.2)
        )

    def get_objectness_label(self,img_shape, gt_boxes, gt_labels, iou_threshold=0.7, anchors=[5,6,25,10,20,34], num_classes=3, downsample=32):
        """
        img 是输入的图像数据，形状是[N, C, H, W]
        gt_boxes，真实框，维度是[N, 50, 4]，其中50是真实框数目的上限，当图片中真实框不足50个时，不足部分的坐标全为0
                  真实框坐标格式是xywh，这里使用相对值
        gt_labels，真实框所属类别，维度是[N, 50]
        iou_threshold，当预测框与真实框的iou大于iou_threshold时不将其看作是负样本
        anchors，锚框可选的尺寸
        anchor_masks，通过与anchors一起确定本层级的特征图应该选用多大尺寸的锚框
        num_classes，类别数目
        downsample，特征图相对于输入网络的图片尺寸变化的比例
        """
        img_shape = img_shape
        batch_size = img_shape[0]
        num_anchors = len(anchors)//2
        input_h = img_shape[2]
        input_w = img_shape[3]
        # 将输入图片划分成num_rows x num_cols个小方块区域，每个小方块的边长是 downsample
        # 计算一共有多少行小方块
        num_rows = input_h//downsample
        # 计算一共有多少列小方块
        num_cols = input_w//downsample
        label_objectness = np.zeros([batch_size, num_anchors, num_rows, num_cols])
        label_classification = np.zeros([batch_size, num_anchors, num_classes, num_rows, num_cols])
        label_location = np.zeros([batch_size, num_anchors, 4, num_rows, num_cols])



        scale_location = np.ones([batch_size, num_anchors, num_rows, num_cols])
        # 对batchsize进行循环，依次处理每张图片
        for n in range(batch_size):

            # 对图片上的真实框进行循环，依次找出跟真实框形状最匹配的锚框
            for n_gt in range(len(gt_boxes[n])):
                gt = gt_boxes[n][n_gt]
                gt_cls = gt_labels[n][n_gt]
                gt_center_x = gt[0]
                gt_center_y = gt[1]
                gt_width = gt[2]
                gt_height = gt[3]
                if (gt_height < 1e-3) or (gt_height < 1e-3):
                    continue
                i = int(gt_center_y * num_rows)
                j = int(gt_center_x * num_cols)
                ious = []
                for ka in range(num_anchors):
                    bbox1 = [0., 0., float(gt_width), float(gt_height)]
                    anchor_w = anchors[ka * 2]
                    anchor_h = anchors[ka * 2 + 1]
                    bbox2 = [0., 0., anchor_w / float(input_w), anchor_h / float(input_h)]
                    # 计算IOU
                    iou = box_iou_xywh(bbox1, bbox2)
                    ious.append(iou)
                ious = np.array(ious)
                inds = np.argsort(ious)
                k = inds[-1]
                label_objectness[n, k, i, j] = 1
                c = gt_cls
                label_classification[n, k, c, i, j] = 1.0.cpu().numpy()

                # for those prediction bbox with objectness =1, set label of location
                dx_label = gt_center_x * num_cols - j
                dy_label = gt_center_y * num_rows - i
                dw_label = np.log(gt_width * input_w / anchors[k * 2])
                dh_label = np.log(gt_height * input_h / anchors[k * 2 + 1])
                label_location[n, k, 0, i, j] = dx_label
                label_location[n, k, 1, i, j] = dy_label
                label_location[n, k, 2, i, j] = dw_label
                label_location[n, k, 3, i, j] = dh_label
                # scale_location用来调节不同尺寸的锚框对损失函数的贡献，作为加权系数和位置损失函数相乘
                scale_location[n, k, i, j] = 2.0 - gt_width * gt_height

        # 目前根据每张图片上所有出现过的gt box，都标注出了objectness为正的预测框，剩下的预测框则默认objectness为0
        # 对于objectness为1的预测框，标出了他们所包含的物体类别，以及位置回归的目标
        return label_objectness.astype('float32'), label_location.astype('float32'), label_classification.astype('float32'), scale_location.astype('float32')




    # 计算某一尺度时的损失
    def loss(self, output, label_objectness, label_location, label_classification, scales, num_anchors,  class_num):
        # 将output从[N, C, H, W]变形为[N, NUM_ANCHORS, NUM_CLASSES + 5, H, W]
        reshaped_output = torch.reshape(output, [-1, num_anchors, 5+class_num, output.shape[2], output.shape[3]])

        # 从output中取出跟objectness相关的预测值
        pred_objectness = reshaped_output[:, :, 4, :, :]
        loss_objectness = torch.nn.functional.binary_cross_entropy_with_logits(pred_objectness,label_objectness)

        # pos_samples 只有在正样本的地方取值为1.，其它地方取值全为0.
        pos_objectness = label_objectness > 0
        pos_samples = pos_objectness.to(torch.float32)
        pos_samples.requires_grad = False

        # 从output中取出所有跟位置相关的预测值
        tx = reshaped_output[:, :, 0, :, :]
        ty = reshaped_output[:, :, 1, :, :]
        tw = reshaped_output[:, :, 2, :, :]
        th = reshaped_output[:, :, 3, :, :]

        # 从gt_box中取出各个位置坐标的标签
        dx_label = label_location[:, :, 0, :, :]
        dy_label = label_location[:, :, 1, :, :]
        dw_label = label_location[:, :, 2, :, :]
        dh_label = label_location[:, :, 3, :, :]

        # 构建损失函数
        loss_location_x = torch.nn.functional.binary_cross_entropy_with_logits(tx, dx_label)
        loss_location_y = torch.nn.functional.binary_cross_entropy_with_logits(ty, dy_label)
        loss_location_w = torch.abs(tw - dw_label)
        loss_location_h = torch.abs(th - dh_label)
        # 计算总的位置损失函数
        loss_location = loss_location_x + loss_location_y + loss_location_w + loss_location_h

        # 乘以scales
        loss_location = loss_location * scales
        # 只计算正样本的位置损失函数
        loss_location = loss_location * pos_samples

        # 从output取出所有跟物体类别相关的像素点
        pred_classification = reshaped_output[:, :, 5:5 + class_num, :, :]
        # 计算分类相关的损失函数
        loss_classification = torch.nn.functional.binary_cross_entropy_with_logits(pred_classification, label_classification)
        loss_classification = torch.sum(loss_classification, axis=2)
        # 只计算objectness为正的样本的分类损失函数
        loss_classification = loss_classification * pos_samples
        total_loss = loss_objectness + loss_classification + loss_location
        # 对所有预测框的loss进行求和
        total_loss = torch.sum(total_loss, axis=[1, 2, 3])
        # 对所有样本求平均
        total_loss = torch.mean(total_loss)
        return total_loss

    # 挑选出跟真实框IoU大于阈值的预测框
    def get_iou_above_thresh_inds(self,pred_box, gt_boxes, iou_threshold):
        batchsize = pred_box.shape[0]
        num_rows = pred_box.shape[1]
        num_cols = pred_box.shape[2]
        num_anchors = pred_box.shape[3]
        ret_inds = np.zeros([batchsize, num_rows, num_cols, num_anchors])
        for i in range(batchsize):
            pred_box_i = pred_box[i]
            gt_boxes_i = gt_boxes[i]
            for k in range(len(gt_boxes_i)):  # gt in gt_boxes_i:
                gt = gt_boxes_i[k]
                gtx_min = gt[0] - gt[2] / 2.
                gty_min = gt[1] - gt[3] / 2.
                gtx_max = gt[0] + gt[2] / 2.
                gty_max = gt[1] + gt[3] / 2.
                if (gtx_max - gtx_min < 1e-3) or (gty_max - gty_min < 1e-3):
                    continue
                x1 = np.maximum(pred_box_i[:, :, :, 0], gtx_min)
                y1 = np.maximum(pred_box_i[:, :, :, 1], gty_min)
                x2 = np.minimum(pred_box_i[:, :, :, 2], gtx_max)
                y2 = np.minimum(pred_box_i[:, :, :, 3], gty_max)
                intersection = np.maximum(x2 - x1, 0.) * np.maximum(y2 - y1, 0.)
                s1 = (gty_max - gty_min) * (gtx_max - gtx_min)
                s2 = (pred_box_i[:, :, :, 2] - pred_box_i[:, :, :, 0]) * (
                            pred_box_i[:, :, :, 3] - pred_box_i[:, :, :, 1])
                union = s2 + s1 - intersection
                iou = intersection / union
                above_inds = np.where(iou > iou_threshold)
                ret_inds[i][above_inds] = 1
        ret_inds = np.transpose(ret_inds, (0, 3, 1, 2))
        return ret_inds.astype('bool')

    #
    def label_objectness_ignore(self, label_objectness, iou_above_thresh_indices):
        negative_indices = (label_objectness < 0.5)
        ignore_indices = negative_indices * iou_above_thresh_indices
        label_objectness[ignore_indices] = -1
        return label_objectness

    # 定义损失函数
    def get_loss(self, outputs, gtbox, gtlabel, gtscore=None, anchors=[[5,6,25,10,20,34],[35,79,52,43,59,115],[115,90,156,197,374,326]],ignore_thresh=0.7):
        self.losses = []
        downsample = [4, 16, 32]
        for i, out in enumerate(outputs):
            label_objectness,label_location,label_classification, scale_location = self.get_objectness_label([out.shape[0],3,416,416], gtbox, gtlabel, iou_threshold=ignore_thresh, anchors=anchors[i],num_classes=self.num_classes, downsample=downsample[i])
            pred_boxes = get_yolo_box_xxyy(out.detach().numpy(),anchors[i],num_classes=self.num_classes, downsample=downsample[i])
            iou_above_thresh_indices = self.get_iou_above_thresh_inds(pred_boxes, gtbox, iou_threshold=0.7)
            label_objectness = self.label_objectness_ignore(label_objectness, iou_above_thresh_indices)

            label_objectness = torch.tensor(label_objectness)
            label_location = torch.tensor(label_location)
            label_classification = torch.tensor(label_classification)
            label_objectness.requires_grad = False
            label_location.requires_grad = False
            label_classification.requires_grad = False
            scale_location = torch.tensor(scale_location)
            scale_location.requires_grad = False

            loss = self.loss(output=out, label_objectness=label_objectness, label_location=label_location, label_classification=label_classification, scales=scale_location, num_anchors=len(anchors[i]//2), class_num=self.num_classes)
            self.losses.append(torch.mean(loss))
        return torch.sum(self.losses)







