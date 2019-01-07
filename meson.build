project('moosic',         version: '0.1.0',
  meson_version: '>= 0.40.0',
)

i18n = import('i18n')

subdir('data')
subdir('moosic')
subdir('po')

meson.add_install_script('build-aux/meson/postinstall.py')

#TODO Are all these gstreamer plugins needed?

dependency('dbus-1')
dependency('libhandy-0.0', version: '>= 0.0.6')
dependency('gstreamer-1.0', version: '>= 1.12')
dependency('gstreamer-base-1.0', version: '>= 1.12')
dependency('gstreamer-audio-1.0', version: '>= 1.12')
dependency('gstreamer-video-1.0', version: '>= 1.12')
dependency('gstreamer-player-1.0', version: '>= 1.12')
dependency('gstreamer-plugins-base-1.0', version: '>= 1.12')
dependency('gstreamer-plugins-bad-1.0', version: '>= 1.12')
dependency('gstreamer-bad-audio-1.0', version: '>= 1.12')
dependency('gstreamer-bad-video-1.0', version: '>= 1.12')