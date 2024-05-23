from typing import Dict

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm


class Trainer:
    def __init__(
        self,
        max_epochs: int,
        loss_fn: nn.Module,
        optim: torch.optim.Optimizer,
        learning_rate: float,
        device: str = "cuda",
    ):
        self.max_epochs = max_epochs
        self.loss_fn = loss_fn
        self.optim = optim
        self.learning_rate = learning_rate
        self.device = device

        self._train_loss = []
        self._train_acc = []
        self._val_loss = []
        self._val_acc = []

        self.train_loss = 0
        self.train_acc = 0
        self.val_loss = 0
        self.val_acc = 0

        self.best_train_loss = float("inf")
        self.best_val_loss = float("inf")

    def train_step(self, batch, batch_idx: int = None):
        # print(f'run step with batch_idx: {batch_idx}')
        X, y = batch
        X = X.to(self.device)
        y = y.to(self.device)
        output = self.model(X)

        loss = self.loss_fn(output, y)
        train_loss = loss.item()

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        y_class = torch.argmax(torch.softmax(output, dim=1), dim=1)
        train_acc = (y_class == y).sum().item() / len(y_class)

        return train_loss, train_acc

    def val_step(self, batch, batch_idx: int = None):
        X, y = batch
        X = X.to(self.device)
        y = y.to(self.device)

        output = self.model(X)
        loss = self.loss_fn(output, y)
        val_loss = loss.item()

        y_class = torch.argmax(torch.softmax(output, dim=1), dim=1)
        val_acc = (y_class == y).sum().item() / len(y_class)

        return val_loss, val_acc

    def train_batch(self, epoch: int = None):
        self.model.train()
        # print(f'run batch with epoch {epoch}')

        train_loss, train_acc = 0, 0

        with tqdm(
            total=len(self.loader.train_loader), desc="Training", leave=False
        ) as pbar:
            for batch_idx, batch in enumerate(self.loader.train_loader):
                _loss, _acc = self.train_step(batch=batch, batch_idx=batch_idx)
                train_loss += _loss
                train_acc += _acc

                pbar.update(1)
                pbar.set_postfix({"loss": _loss})

        avg_loss = train_loss / len(self.loader.train_loader)
        avg_acc = train_acc / len(self.loader.train_loader)

        return avg_loss, avg_acc

    def val_batch(self, epoch: int = None):
        self.model.eval()

        val_loss, val_acc = 0, 0
        with tqdm(
            total=len(self.loader.valid_loader), desc="Validation", leave=False
        ) as pbar:
            with torch.no_grad():
                for batch_idx, batch in enumerate(self.loader.valid_loader):
                    _loss, _acc = self.val_step(batch=batch, batch_idx=batch_idx)
                    val_loss += _loss
                    val_acc += _acc

                    pbar.update(1)
                    pbar.set_postfix({"loss": _loss})

        avg_loss = val_loss / len(self.loader.valid_loader)
        avg_acc = val_acc / len(self.loader.valid_loader)

        return avg_loss, avg_acc

    def run(self):
        total_steps = self.max_epochs * len(self.loader.train_loader)

        with tqdm(total=total_steps, desc="Epochs") as pbar:
            for epoch in range(self.max_epochs):
                print(f"Epoch {epoch+1}/{self.max_epochs}")
                self.train_loss, self.train_acc = self.train_batch(epoch)
                self.val_loss, self.val_acc = self.val_batch(epoch)

                self._train_loss.append(self.train_loss)
                self._val_loss.append(self.val_loss)
                self._train_acc.append(self.train_acc)
                self._val_acc.append(self.val_acc)

                if (
                    self.train_loss < self.best_train_loss
                    and self.val_loss < self.best_val_loss
                ):
                    self.best_train_loss = self.train_loss
                    self.best_val_loss = self.val_loss

                    self.save_model(self.path_to_save)

                pbar.update(1)
                pbar.set_postfix(
                    {"train_loss": self.train_loss, "val_loss": self.val_loss}
                )

    def save_model(self, path_to_save):
        self.path_to_save = path_to_save
        torch.save(self.model.state_dict(), self.path_to_save)
        print(
            f"[INFO] Save model with train loss: {self.train_loss}, and val loss: {self.val_loss}"
        )

    def fit(self, model: nn.Module, loader: DataLoader) -> Dict[str, float]:
        self.model = model.to(self.device)
        self.loader = loader
        self.run()
