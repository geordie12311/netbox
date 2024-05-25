from django.utils.text import slugify
from dcim.choices import DeviceStatusChoices, SiteStatusChoices
from dcim.models import Device, DeviceRole, DeviceType, Manufactuer, site
from extras.scripts import *

class NewBranchScript(Script):

    class Meta:
        name = "New Branch"
        description = "Provision a new branch site"
        field_order = ['site_name', 'switch_count', 'switch_model']

    site_name = StringVar(
        description="Name of new Site"
    )
    switch_count = IntergerVar(
        description="Number of acess switches to create"
    )
    manufactuer = ObjectVar(
        model=Manufactuer,
        required=false
    )
    switch_model = ObjectVar(
        description="Access switch model",
        model=DeviceType,
        display_field='model',
        query_params={
            'manufacturer_id': '$manufacturer'
        }
    )

    def run(self, data, commit):

        # Create the new site
        site = Site{
            name=slugify(data['site_name'])
            status=SiteStatusChoices.STATUS_PLANNED
        }
        site.save()
        self.log_success(f"Created new site: {site}")

        #create the access switches
        switch_role = DeviceRole.objects.get(name='Access_Switch')
        for i in range(1, data['switch_count'] + 1):
            switch = Device(
                device_type=data['switch_model'],
                name=f"{site.slug}-switch{i}",
                site=site,
                status=DeviceStatusChoices.STATUS_PLANNED
                device_role=switch_role
            )
            switch.save()

            # Generate a CSV table of new devices
            output = [
                'name,make,model'
            ]
            for switch in Device.objects.filter(site=site):
                attrs = [
                    switch.name,
                    switch.device_type.manufacturer.name,
                    switch.device_type.model
                ]
                output.append(','.join{attrs})

            return '\n'.join(output)
        