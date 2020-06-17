project('Moozik',
	version: '0.1.0',
  	meson_version: '>= 0.40.0',
)

application_id = 'org.gnome.Moozik'

i18n   = import('i18n')
python = import('python3')

message('Looking for dependencies')
python_bin = python.find_python()
if not python_bin.found()
    error('No valid python3 binary found')
endif
dependency('glib-2.0')
dependency('gobject-2.0')
dependency('gobject-introspection-1.0')
dependency('gtk+-3.0', version :'>=3.16')
dependency('libhandy-1', version :'>=0.81')

BIN_DIR    = join_paths(get_option('prefix'), get_option('bindir'))
PYTHON_DIR = join_paths(get_option('prefix'), python.sysconfig_path('purelib'))
DATA_DIR   = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
LOCALE_DIR = join_paths(get_option('prefix'), get_option('datadir'), 'locale')

conf = configuration_data()
conf.set('DATA_DIR', DATA_DIR)
conf.set('LOCALE_DIR', LOCALE_DIR)
conf.set('PYTHON_DIR', PYTHON_DIR)
conf.set('VERSION', meson.project_version())
conf.set('PROJECT_NAME', meson.project_name())
conf.set('LIBDIR', join_paths(get_option('prefix'), get_option('libdir')))

subdir('data')
subdir('po')

dependency('dbus-1')
dependency('gstreamer-1.0', version: '>= 1.12')
dependency('gstreamer-base-1.0', version: '>= 1.12')
dependency('gstreamer-audio-1.0', version: '>= 1.12')
dependency('gstreamer-player-1.0', version: '>= 1.12')
dependency('gstreamer-plugins-base-1.0', version: '>= 1.12')
dependency('gstreamer-plugins-bad-1.0', version: '>= 1.12')
dependency('gstreamer-bad-audio-1.0', version: '>= 1.12')

install_subdir(
  'Moozik',
  install_dir: PYTHON_DIR
)

configure_file(
  input: 'moozik.py.in',
  output: 'moozik',
  configuration: conf,
  install_dir: BIN_DIR
)

meson.add_install_script('build-aux/meson/postinstall.py')
