import os
from pathlib import Path
from abc import abstractmethod

import torch


class BaseTrainer:
    def __init__(
        self,
        model,
        optimizer,
        *,
        epochs: int,
        save_dir: str,
        save_period: int,
    ) -> None:
        # TODO: Implement logging

        self.model = model
        self.optimizer = optimizer

        self.epochs = epochs
        self.start_epoch = 1
        self.checkpoint_dir = Path(save_dir)
        self.save_period = save_period

    @abstractmethod
    def _train_epoch(self, epoch):
        raise NotImplementedError

    def train(self):
        for epoch in range(self.start_epoch, self.epochs + 1):
            _ = self._train_epoch(epoch)

            if epoch % self.save_period == 0:
                self._save_checkpoint(epoch)

    def _save_checkpoint(self, epoch):
        arch = type(self.model).__name__
        optimizer_type = type(self.optimizer).__name__

        state = {
            'arch': arch,
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'optimizer_type': optimizer_type,
        }
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        filename = self.checkpoint_dir / f'checkpoint-epoch{epoch}.pth'
        torch.save(state, filename)

    def _resume_checkpoint(self, resume_path):
        resume_path = str(resume_path)
        checkpoint = torch.load(resume_path)

        self.start_epoch = checkpoint['epoch'] + 1
        checkpoint_arch = checkpoint['arch']
        arch = type(self.model).__name__
        if checkpoint_arch != arch:
            raise ValueError(
                "Trainer's model architecture differs from checkpoint's.")
        self.model.load_state_dict(checkpoint['state_dict'])

        checkpoint_optimizer_type = checkpoint['optimizer_type']
        optimizer_type = type(self.optimizer).__name__
        if checkpoint_optimizer_type != optimizer_type:
            raise ValueError("Trainer's optimizer differs from checkpoint's.")
        self.optimizer.load_state_dict(checkpoint['optimizer'])
