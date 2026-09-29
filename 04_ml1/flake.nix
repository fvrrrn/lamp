{
  description = "ML1 development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {
      inherit system;
    };

  in {
    devShells.${system} = {
      default = pkgs.mkShell {
        # graphviz provides the `dot` binary that torchviz shells out to
        packages = [pkgs.graphviz];

        # the uv-managed CPython has no CA bundle baked in, so HTTPS reads
        # (pandas.read_csv of a URL, torchvision downloads) fail without this
        # (nix develop filters SSL_CERT_FILE out of plain attrs, hence the hook)
        shellHook = ''
          export SSL_CERT_FILE="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
        '';
      };
    };
  };
}
