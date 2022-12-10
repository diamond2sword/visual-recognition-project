



def print_pic(pic):
    pic = to_printable_image(pic)
    pic.draw()
    pass


def print_str(string):
    print(string)


from term_image.image import AutoImage as to_printable_image
