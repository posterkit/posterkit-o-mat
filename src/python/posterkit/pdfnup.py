# -*- coding: utf-8 -*-
# (c) 2018 The PosterKit developers <developers@posterkit.org>
"""
# Layout multiple pages in matrix
pdfnup --nup 2x3 --landscape=true --no-tidy lqdn-gafam-poster-de.pdf

# Convert to GIF format appropriately
convert -units PixelsPerInch lqdn-gafam-poster-de-nup.pdf -density 72 -trim +repage -resize 595x gafam-german-card.gif
"""
import os
import logging
import tempfile

from io import BytesIO

logger = logging.getLogger(__name__)

# Use False for debugging to keep all temporary files
DELETE_TEMPFILES = True


def create_image(pdf_file, nup='1', size='1024x', format='jpg'):

    logger.info('Creating thumbnail image for {}'.format(pdf_file))

    tmp_nupped = tempfile.NamedTemporaryFile(suffix='.pdf', delete=DELETE_TEMPFILES)
    output_file = tmp_nupped.name

    # Run "pdfnup" for tiled layout
    # TODO: Add "--no-tidy" for debugging
    command = "pdfnup --papersize '{{297mm,1050mm}}' --nup {nup} --vanilla --keepinfo --outfile '{output_file}' '{pdf_file}'".format(**locals())
    logger.info('Running "pdfnup" command: {}'.format(command))
    os.system(command)

    input_file = tmp_nupped.name
    tmp_image = tempfile.NamedTemporaryFile(delete=DELETE_TEMPFILES)
    output_file = tmp_image.name

    # Dumb trimming
    #repage_option = "+repage"

    # Trimming with a Specific Color
    # http://www.imagemagick.org/Usage/crop/#trim_color
    #repage_option = "-set page '%[fx:page.width-2]x%[fx:page.height-2]+%[fx:page.x-1]+%[fx:page.y-1]'"
    #repage_option = ""

    #command = "convert -units PixelsPerInch '{input_file}' -density 300 -trim +repage -resize {size} '{output_file}'".format(**locals())
    #command = "convert -units PixelsPerInch '{input_file}' -density 300 -trim {repage_option} -crop -10-10\! -resize {size} '{format}:{output_file}'".format(**locals())
    command = "convert -units PixelsPerInch '{input_file}' -density 300 -filter Lanczos -resize {size} '{format}:{output_file}'".format(**locals())
    logger.info('Running "convert" command: {}'.format(command))
    os.system(command)

    tmp_image.seek(0)
    buffer = BytesIO(tmp_image.read())
    return buffer
