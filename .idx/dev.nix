# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env

{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-25.05"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python312
    pkgs.uv
    pkgs.ruff
  ];
  # Sets environment variables in the workspace
  env = {};
  # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
  idx.extensions = [
      "ms-python.python"
      "ms-toolsai.jupyter"
      "ms-python.vscode-pylance"
      "charliermarsh.ruff"
      "Google.validation-agent-extension"
      "ms-python.debugpy"
    ];
    idx = {
      workspace = {
      # Runs when a workspace is first created with this `dev.nix` file
        onCreate = {
          create-venv = ''
            uv venv
            source .venv/bin/activate
            uv pip install -r pyproject.toml
            '';
          # Open editors for the following files by default, if they exist:
          default.openFiles = [ "00-adk-intro/adk00_template/agent.py" ];
          };
      # To run something each time the workspace is (re)started, use the `onStart` hook
        };
    # Enable previews and customize configuration
  previews = {};
    };
}
