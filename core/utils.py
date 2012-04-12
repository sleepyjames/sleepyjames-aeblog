from django.template.defaultfilters import slugify


def make_slug_for_model(instance, src_field, dest_field, max_length=100):
    """ Create a unique slug based on an entity property
    """

    slug_from_value = getattr(instance, src_field) 

    # Keep correct length
    pre_slug = slugify(slug_from_value)
    try_slug = pre_slug[:max_length-1]
    slug = try_slug

    qs = instance.__class__.all()

    if instance.is_saved():
        qs = qs.filter('__key__ !=', instance.key())

    if qs.count() > 0:

        allslugs = [s.slug for s in qs]

        if try_slug in allslugs:
            counter = 2
            slug = "%s-%i" % (pre_slug[:max_length-2], counter)
            while slug in allslugs:
                trim_length = len(str(counter)) + 1
                slug = "%s-%i" % (pre_slug[:max_length-trim_length], counter)
                counter += 1

    setattr(instance, dest_field, slug)

