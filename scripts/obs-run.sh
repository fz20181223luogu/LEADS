if ! sudo -v &>/dev/null;
then
  echo "the script requires sudo"
  exit 1
fi
sudo MESA_GL_VERSION_OVERRIDE=3.3 obs