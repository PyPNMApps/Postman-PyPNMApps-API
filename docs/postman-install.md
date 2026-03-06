# Install Postman Desktop (Ubuntu and Windows)

## Required Version

- Use **Postman Desktop v12 or newer** for this repository.
- This repo uses local-mode YAML collections (`*.request.yaml`) aligned with Postman Collection v3 workflows.

## Download

- Official Postman downloads page: `https://www.postman.com/downloads/`

## Windows

1. Open the Postman downloads page.
2. Download the **Windows 64-bit** desktop installer.
3. Run the installer.
4. Launch Postman and sign in (optional).

## Ubuntu (Desktop)

Use the Postman downloads page to get the Linux desktop package, then install it.

Common install flow (tarball-based):

1. Download the Linux package from the Postman downloads page.
2. Extract it.
3. Launch the Postman executable from the extracted directory.

Example commands (adjust the filename if needed):

```bash
cd ~/Downloads
tar -xzf postman-linux-x64.tar.gz
./Postman/Postman
```

Optional (system-wide install location):

```bash
sudo rm -rf /opt/Postman
sudo mv ~/Downloads/Postman /opt/Postman
/opt/Postman/Postman
```

## Verify

- Postman Desktop opens successfully
- You can access the `Import` button in the app UI

## Next Step

- Continue with `docs/user-guide.md` to import the PyPNM Postman collections and configure globals.
