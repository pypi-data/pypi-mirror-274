from distutils.core import setup
setup(
  name = 'udirect',         # How you named your package folder (MyLib)
  packages = ['udirect'],   # Chose the same as "name"
  version = '0.1.4-dev.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Deep learning tools for modeling rupture forward directivity',   # Give a short description about your library
  author = 'Henning Lilienkamp',                   # Type in your name
  author_email = 'henninglilienkamp@gmx.de',      # Type in your E-Mail
  url = 'https://github.com/HenningLilienkamp/udirect',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/HenningLilienkamp/udirect/archive/refs/tags/v.0.1.tar.gz',    # I explain this later on
  keywords = ['Deep learning', 'Rupture forward directivity', 'Modifier of moments'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'tensorflow',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',   # Again, pick a license

    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.9',
  ],
  package_data={'udirect' :['directivity_model/*', 'directivity_model/variables/*']},
  include_package_data=True,
)