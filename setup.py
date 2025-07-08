from setuptools import setup, find_packages

setup(
    name='Ai_Smartcontract_Auditor',
    version='0.1.0',
    description='AI-powered autonomous C++ smart contract auditor for the Qubic Network.',
    author='Andromeda Qubic Track',
    packages=find_packages(include=["agents*", "frontend*", "mcp*", "your_llm*"]),  # explicitly include all relevant folders
    include_package_data=True,
    install_requires=[
        'streamlit',
        'openai',
        'tiktoken',
        'pygments',
        'jinja2',
        'pdfkit',
        'reportlab',
        'fpdf',             # ✅ for FPDF (version 1.x) - use 'fpdf2' only if using that version
        'fpdf2',            # ✅ optional, if you're using newer syntax from fpdf2
        'python-dotenv',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'defi-sentinel=main:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
