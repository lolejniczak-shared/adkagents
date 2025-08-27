# No user-configurable parameters
{ pkgs, ... }: {
  packages = [
    pkgs.python312
  ];
  bootstrap = ''
    cp -rf ${./.} "$out"
    chmod -R +wx "$out"
    rm -rf "$out/.git" "$out/idx-template".{nix,json}
  '';
}