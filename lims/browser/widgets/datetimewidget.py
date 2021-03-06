from dependencies.dependency import ClassSecurityInfo
from dependencies.dependency import TypesWidget
from dependencies.dependency import registerWidget
from dependencies.dependency import registerPropertyType
from lims.browser import ulocalized_time as ut


class DateTimeWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'show_time': False,
        'macro': "bika_widgets/datetimewidget",
        'helper_js': ("bika_widgets/datetimewidget.js",),
        'helper_css': ("bika_widgets/datetimewidget.css",),
    })

    security = ClassSecurityInfo()

    def ulocalized_time(self, time, context, request):
        val = ut(time,
                 long_format=self._properties['show_time'],
                 time_only=False,
                 context=context,
                 request=request)
        return val


registerWidget(
    DateTimeWidget,
    title='DateTimeWidget',
    description=('Simple text field, with a jquery date widget attached.')
)

registerPropertyType('show_time', 'boolean')
