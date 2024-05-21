from setuptools import setup, find_packages


setup(name='MRISegmentator',
        version='0.1.0',
        description='Robust segmentation of 62 abdominal structures on MRI T1 Weighted images.',
        long_description="See https://arxiv.org/abs/2405.05944.",
        url='https://github.com/wasserth/TotalSegmentator',
        author='Yan Zhuang and Abhinav Suri',
        author_email='rsummers@nih.gov',
        python_requires='>=3.9',
        license='Apache 2.0',
        packages=find_packages(),
        install_requires=[
            'torch>=2.0.0',
            'tqdm>=4.45.0',
            'p_tqdm',
            'nnunetv2>=2.2.1',
        ],
        zip_safe=False,
        classifiers=[
            'Intended Audience :: Science/Research',
            'Programming Language :: Python',
            'Topic :: Scientific/Engineering',
        ],
        entry_points={
            'console_scripts': [
                'MRISegmentator=mrisegmentator.cmdline:main',
            ],
        },
    )