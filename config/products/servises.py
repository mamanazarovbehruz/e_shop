def upload_protuctItem_path(instance, image):

    return f'productItemImage/{instance.title}/{image}'

def upload_protuctItem_small(instance, image):

    return f'productItemImage/imageSmall/{instance.title}/{image}'

def upload_protuctItem_medium(instance, image):

    return f'productItemImage/imageMedium/{instance.title}/{image}'

def upload_protuctItem_large(instance, image):

    return f'productItemImage/imageLarge/{instance.title}/{image}'

def upload_brand_path(instance, image):

    return f'brandImage/{instance.name}/{image}'

def upload_category_path(instance, image):

    return f'categoryImage/{instance.title}/{image}'