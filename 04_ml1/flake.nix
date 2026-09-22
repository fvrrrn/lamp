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
      };
    };
  };
}
