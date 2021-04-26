# po-language-server

This is a work-in-progress Markov-chain based completion language server for `po` files.

## Issues

At the moment it loads properly for `po-mode`, but it does *not* load
on Text buffer opened by `po-mode` to edit `msgid`s.


## Installation

Just run `python3 -m pip install .`.


## Emacs configuration

I did not (yet?) packaged it, but it's not that hard to configure:

```
(add-to-list 'lsp-language-id-configuration '(po-mode . "gettext"))

(lsp-register-client
 (make-lsp-client
  :new-connection (lsp-stdio-connection "po-langage-server")
  :activation-fn (lsp-activate-on "gettext" "plaintext")
  :priority -1
  :server-id 'po
))
(add-hook 'po-mode-hook #'lsp)
(add-hook 'text-mode-hook #'lsp)

(add-to-list 'lsp-enabled-clients 'po)
```
