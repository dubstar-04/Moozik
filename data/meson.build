gnome = import('gnome')

message('Compiling resources')

gnome.compile_resources(
  meson.project_name(),
  application_id + '.gresource.xml',
  gresource_bundle: true,
  source_dir: '.',
  install_dir: DATA_DIR,
  install: true
)

message('Compiling schemas')
gnome.compile_schemas()
install_data(
  application_id + '.gschema.xml',
  install_dir: join_paths(get_option('prefix'), 'share/glib-2.0/schemas')
)

message('Making a .desktop file')
desktop_conf = configuration_data()
desktop_conf.set('icon', application_id)
i18n.merge_file(
  type: 'desktop',
  input: configure_file(
    output: application_id + '.desktop.in',
    input: application_id + '.desktop.in.in',
    configuration: desktop_conf),
  output: application_id + '.desktop',
  po_dir: join_paths(meson.source_root(), 'po'),
  install: true,
  install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'applications')
)

message('Preparing appdata')
i18n.merge_file(
  output: application_id + '.appdata.xml',
  input: application_id + '.appdata.xml.in',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')

)

# Installing the icons
icon_sizes = ['scalable']

foreach i : icon_sizes
  install_data(
    join_paths('icons/hicolor/', i , 'apps', application_id  + '.svg'),
    install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'icons', 'hicolor', i , 'apps'),
    rename: '@0@.svg'.format(application_id )
  )
endforeach

# Installing the symbolic icon
install_data(
    join_paths('icons/hicolor/symbolic/apps', application_id  + '-symbolic.svg'),
    install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'icons/hicolor/symbolic/apps'),
    rename: '@0@-symbolic.svg'.format(application_id)
)
