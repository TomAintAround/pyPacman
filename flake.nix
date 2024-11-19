{
    description = "IPRP shell";

    inputs = {
        nixpkgs.url = "github:NixOs/nixpkgs/nixos-unstable";
    };

    outputs = inputs: let
        system = "x86_64-linux";
        pkgs = import inputs.nixpkgs {
            inherit system;
            config.allowUnfree = true;
        };
    in {
        devShells.${system}.default =
            pkgs.mkShell {
                packages = with pkgs; [
                    python3
                    python312Packages.tkinter
                ];
            };
    };
}
