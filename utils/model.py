import torch
import torchvision.models as models
from torch.nn import Module, Linear, Sequential, BatchNorm1d
from torchvision.models import resnet50, VGG16_BN_Weights, ResNet50_Weights

from utils import args


def get_output_classes():
    if args.dataset == 'CIFAR10':
        return 10
    elif args.dataset == 'CIFAR100':
        return 100
    else:
        raise RuntimeError(f"Output class count for {args.dataset} was not defined.")


class VGG(Module):
    def __init__(self, output_classes=10, pretrained=False):
        super(VGG, self).__init__()
        self.features = models.vgg16_bn(weights=VGG16_BN_Weights.DEFAULT if pretrained else None).features
        
        self.classifier = Sequential(
            Linear(512, 512),
            BatchNorm1d(512),
            Linear(512, output_classes)
        )
        
    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x


def get_model():
    pretrained = args.pretrained and not args.load_path
    if args.model == 'VGG':
        network = VGG(output_classes=get_output_classes(), pretrained=pretrained)
    else:  # args.model == 'ResNet'
        network = resnet50(weights=ResNet50_Weights.DEFAULT if pretrained else None)
        network.fc = Linear(network.fc.in_features, get_output_classes())

    if args.load_path:
        checkpoint = torch.load(args.load_path)
        network.load_state_dict(checkpoint['state_dict'])

    return network
