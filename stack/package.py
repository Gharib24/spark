import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from datastore import software_questions as questions
#--------------------------------------------------------------------------------------------------

class PackageSelection:

	def __init__(self):
		super().__init__()

	def package(self):
		table = Gtk.Table(rows=20, columns=3, homogeneous=False)
		table.set_col_spacings(15)
		table.set_row_spacings(15)
		table.props.border_width = 10
		table.attach(Gtk.Label(), 1, 3, 0, 1, xoptions=Gtk.AttachOptions.EXPAND ,yoptions=Gtk.AttachOptions.FILL)

		stack_name = str(self.category.index("Package Selection"))
		self.stack_1.add_named(table, stack_name)

		label_name = ['Install software ', 'Install additional packages', 'Upgrade packages']

		label = Gtk.Label(label_name[0], xalign=0, yalign=0.5)
		table.attach(label, 0, 1, 0, 1, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)

		tasksel = ['desktop', 'gnome-desktop', 'xfce-desktop',
			'kde-desktop', 'cinnamon-desktop', 'mate-desktop', 'lxde-desktop',
			'lxqt-desktop', 'web-server', 'print-server', 'ssh-server', 'laptop', 'standard']

		tasksel_name = ['Debian desktop environment',
			 'Gnome desktop','Xfce desktop',
			'KDE Plasma desktop','Cinnamon desktop',
			'MATE desktop' , 'LXDE desktop',
			'LXQt desktop', 'Web server',
			'Print server', 'SSH server',
			'Laptop', 'Standard tools']

		self.package_liststore = Gtk.ListStore(bool, str, str,)
		for column1, column2 in zip(tasksel, tasksel_name):
			self.package_liststore.append([False, column1, column2 ])

#		frame = Gtk.AspectFrame(label= None, xalign=0.0, yalign=0.0, ratio=1, obey_child=1)
		scrolled_window = Gtk.ScrolledWindow()
		scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_window.set_border_width(0)

		frame = Gtk.Frame(label=None)
		frame.props.border_width = 5
		frame.add(scrolled_window)
		table.attach(frame, 1, 3, 0, 18, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
		view = Gtk.TreeView(model = self.package_liststore)
		scrolled_window.add(view)
		view.set_hexpand (False)
		view.set_vexpand (True)
		view.set_headers_visible(False)
#		self.view_selection = view.get_selection()
#		self.view_selection.connect("changed", self.on_view_selection_changed)
		renderer_toggle = Gtk.CellRendererToggle(xalign=0, yalign=0.7)
		renderer_toggle.connect("toggled", self.on_cell_toggled , questions[0])
		column_toggle = Gtk.TreeViewColumn("select", renderer_toggle, active=0)
		column_toggle.set_min_width(10)
		column_toggle.set_reorderable(False)
#		column_toggle.set_sizing()
		view.append_column(column_toggle)
		renderer = Gtk.CellRendererText()
		renderer.set_fixed_size(250, height=24)
		renderer.set_alignment(xalign=0.0 , yalign=0.5)
#		column1 = Gtk.TreeViewColumn('tasksel', renderer, text=1)
		column2 = Gtk.TreeViewColumn('tasksel name', renderer, text=2)
#		column2.set_min_width(80)
#		column1.set_reorderable(True)
#		view.append_column(column1)
		view.append_column(column2)
		self.id[questions[0]] = renderer_toggle


		separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
		table.attach(separator, 0, 3, 18, 19, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)

		label = Gtk.Label(label_name[1], xalign=0, yalign=0.6)
		table.attach(label, 0, 1, 19, 20, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)

		frame = Gtk.Frame(label=None)
		frame.props.border_width = 0
		table.attach(frame, 1, 3, 19 , 25, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)

		scrolled_window = Gtk.ScrolledWindow()
		scrolled_window.set_border_width(0)
		scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		frame.add(scrolled_window)

		self.buffer = Gtk.TextBuffer()
		self.buffer.connect( "changed", self.on_text_changed, questions[1]) 
		#self.buffer.set_text('')
		self.textview = Gtk.TextView(buffer=self.buffer)
		self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
		scrolled_window.add(self.textview)

		label = Gtk.Label(label_name[2], xalign=0, yalign=0.5)
		table.attach(label, 0, 1, 26 , 27, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
		self.id[questions[1]] = self.buffer

		comboboxtext = Gtk.ComboBoxText()
		#comboboxtext.set_sensitive(False)
		comboboxtext.append("safe-upgrade", "Safe upgrade")
		comboboxtext.append("full-upgrade", "Full upgrade")
		comboboxtext.append("none", "None")
#		comboboxtext.set_active_id("safe-upgrade")
		table.attach(comboboxtext, 1, 3, 26 , 27, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
		comboboxtext.connect("changed",self.on_comboboxtext_changed, questions[2])
		self.id[questions[2]] = comboboxtext

