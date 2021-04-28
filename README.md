# po-language-server

This is a Markov-chain based completion [language
server](https://github.com/Microsoft/language-server-protocol/) for
gettext `po` files.

![](https://mdk.fr/po-language-server.gif)


## Installation

`python3 -m pip install po-language-server`

It should be compatible with vim, emacs, vscode, and other text
editors acting as language server clients. I only tried it using emacs
though.


## Emacs configuration

I did not packaged it yet (feel free to help), but it's not that hard
to configure:

```
(require 'lsp-mode)

(add-to-list 'lsp-language-id-configuration '(po-mode . "gettext"))

(lsp-register-client
 (make-lsp-client
  :new-connection (lsp-stdio-connection "po-language-server")
  :activation-fn (lsp-activate-on "gettext" "plaintext")
  :priority -1
  :server-id 'po
))
(add-hook 'po-mode-hook #'lsp)

;; lsp-mode can only work on named buffers
(defun po-mode-name-buffer ()
  (setq-local buffer-file-name "msgstr.po")
  (lsp))

(defun po-mode-unname-buffer ()
  (setq-local buffer-file-name nil))

(add-hook 'po-mode-hook
 (lambda ()
   (advice-add 'po-edit-msgstr :after 'po-mode-name-buffer)
   (advice-add 'po-subedit-exit :before 'po-mode-unname-buffer)))

(add-to-list 'lsp-enabled-clients 'po)
```
