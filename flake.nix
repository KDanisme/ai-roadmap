{
  outputs = inputs:
    inputs.flake-parts.lib.mkFlake {inherit inputs;} {
      systems = inputs.nixpkgs.lib.systems.flakeExposed;
      imports = [
        inputs.flake-root.flakeModule
        inputs.treefmt-nix.flakeModule
        inputs.pre-commit-hooks.flakeModule
        # inputs.process-compose-flake.flakeModule
      ];
      perSystem = {
        pkgs,
        config,
        ...
      }: {
        pre-commit.settings.hooks.treefmt.enable = true;
        treefmt.config = {
          inherit (config.flake-root) projectRootFile;
          programs = {
            alejandra.enable = true;
            shellcheck.enable = true;
            black.enable = true;
          };
        };
        devShells.default = pkgs.mkShell {
          inputsFrom = [config.pre-commit.devShell];
          packages = [
            (pkgs.python3.withPackages (p: with p; [debugpy scikit-learn numpy pandas matplotlib]))
          ];
        };
      };
    };
  inputs = {
    nixpkgs.url = "nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    flake-root.url = "github:srid/flake-root";
    pre-commit-hooks = {
      url = "github:cachix/pre-commit-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    treefmt-nix = {
      url = "github:numtide/treefmt-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
}
