
### jabir
We developed the Python package named **jabir** to generate atomic features. It can generate **322 atomic features for any type of material**, such as Electron Affinity, Electric Polarizability, Thermal Conductivity, Pettifor number, etc. Jabir calculates statistical relationships for each physical and chemical feature based on Element, Subscript, and Fraction.

### Installation
**Jabir** employs some other libraries and packages to generate atomic features of materials, which need to be installed. These packages consist of **pandas**, **numpy**, **mendeleev**, **pymatgen** and **tqdm**. Therefore, it’s necessary to install all these packages. If you encounter an error, it is probably due to the conflict of different versions of the packages, so be sure to install the following versions using the commands below:
pip install mendeleev==0.16.1 , pip install pymatgen==2024.5.1 , pip install tqdm==4.66.4

**Note:** If you encounter any difficulties installing these packages on your local system, you can utilize the **Google colab** environment to install and utilize them seamlessly.

### How to use jabir
After installing jabir, simply execute the following two lines of code.
> from jabir import main 

> print(main())
