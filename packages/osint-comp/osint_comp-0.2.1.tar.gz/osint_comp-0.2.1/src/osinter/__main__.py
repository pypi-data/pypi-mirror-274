import rich_click as click
import os
from rich import print as rprint
from rich.console import Console
from rich.table import Table

formatkeys = ["n","nf","nma","nm","nl","a","al","ac","as","an","az","aa","fb","in","tx","rd","li","tt"]

# osinter reader legend; line in corresponding file; top-level format
# n is full name; line 1; nf (if no nm, nma, if no nma, leave blank) nl
# nf is first name; line 2
# nma is middle name abbrevated; line 3
# nm is middle name; line 4
# nl is last name; line 5

# a is full address; line 1; al (aa), ac, as, an
# al is address line; line 2
# ac is address city; line 3
# as is address state( or province); line 4
# an is address nation; line 5
# az is address zip code; line 6
# aa is apartment number; line 7


@click.group()
def cli():
    pass

@cli.command()
@click.option("--file", "-f", type=str, help="Name of new file", default="")
def new(file):
    """Creates a new osint file"""
    os.system("clear")
    rprint("[bold]Welcome to OSINTer[/]\n\n")
    if file == "":
        file = click.prompt("What would you like to name the file?\n (name is used to read it later)\n")
        if os.path.exists(f"osint/{file}"):
            raise click.ClickException(f"A file with the name {file} already exists.")
    else:
        if os.path.exists(f"osint/{file}"):
            raise click.ClickException(f"A file with the name {file} already exists.")        
    os.mkdir(f"osint/{file}")
    os.system(f"touch osint/{file}/init.oie")
    os.system(f"touch osint/{file}/name.oie")
    os.system(f"touch osint/{file}/address.oie")
    os.system(f"touch osint/{file}/online")
    os.system(f"touch osint/{file}/online/usernames.oie")
    os.system(f"touch osint/{file}/online/emails.oie")
    fn = open(f"osint/{file}/name.oie", "a")
    fa = open(f"osint/{file}/address.oie", "a")
    fos = open(f"osint/{file}/online/socials.oie", "a")
    fn.write("\n\n\n\n\n")
    fa.write("\n\n\n\n\n\n\n")
    fos.write("\n\n\n\n\n\n")
    fn.close()
    fa.close()
    rprint("Files created!")
    exit()
    
    

@cli.command()
def setup():
    """Sets up the osint directories"""
    os.system("clear")
    rprint("[bold]Welcome to OSINTer[/]\n\n")
    if not os.path.exists("osint"):
        click.echo("Would you like to create the osint file?\nThis is where all of the directories and files will be stored. ")
        create = click.prompt("(y/n) ")
        if create == "y":
            os.mkdir("osint")
            f = open("osint/readme.md", "w")
            f.write("# OSINTer File Storage\n\nIt's best not to change with any files in this directory, as it can mess up the OSINTer program.")
            f.close()
            click.echo("Setup complete!")
            exit()
        elif create == "n":
            click.echo("Okay, exiting...")
            exit()
    else:
        click.echo("It seems like you already have setup your files")
        click.echo("If you would like to reset you files, use")
        click.echo("osint reset")
        exit()

@cli.command()
def reset():
    """Removes the osint directories, clearing all data"""
    click.clear()
    click.echo("Are you sure you want to reset? This will delete all your osint files")
    check = click.prompt("(y/n) ")
    if check == "y":
        click.echo("Deleting...")
        os.system("rm -rf osint")
        click.echo("Reset complete")
        click.echo("I suggest you to use osint setup to set it up again")
        exit()
    elif check == "n":
        click.echo("Okay, exiting...")
        exit()

@cli.command()
@click.option("--table", "-t", help="Picks which specific table to show.\na for address\nn for name\n- for all tables\nDefaults to -", nargs=1, default="-")
@click.option("--file", "-f", type=str, help="Name of the file to read", default="")
def read(table, file):
    """Reads the osint file, and puts in a nice table"""
    os.system("clear")
    rprint("[bold]Welcome to OSINTer[/]\n\n")
    if file == "":
        click.echo("What file would you like to read?")
        file = click.prompt("File name")
        click.echo("\n")
    ndata = {"n": "",
            "nf":"",
            "nma":"",
            "nm":"",
            "nl":""}
    adata = {
        "a": "",
        "al": "",
        "ac": "",
        "as": "",
        "an": "",
        "az": "",
        "aa": ""
    }
    if os.path.exists("osint/" + file):
        fn = open(f"osint/{file}/name.oie", "r") # name file
        fa = open(f"osint/{file}/address.oie", "r") # address file
        ntable = Table(title=f"OSINT Name File: {file}")
        atable = Table(title=f"OSINT Address File: {file}")
        ntable.add_column("Key", justify="center")
        ntable.add_column("Value", justify="center")
        atable.add_column("Key", justify="center")
        atable.add_column("Value", justify="center")
        n = fn.readlines()
        a = fa.readlines()
        ndata["n"] = n[0] if not None else "Not found"
        ndata["nf"] = n[1] if not None else "Not found"
        ndata["nma"] = n[2] if not None else "Not found"
        ndata["nm"] = n[3] if not None else "Not found"
        ndata["nl"] = n[4] if not None else "Not found"
        adata["a"] = a[0] if not None else "Not found"
        adata["al"] = a[1] if not None else "Not found"
        adata["ac"] = a[2] if not None else "Not found"
        adata["as"] = a[3] if not None else "Not found"
        adata["an"] = a[4] if not None else "Not found"
        adata["az"] = a[5] if not None else "Not found"
        adata["aa"] = a[6] if not None else "Not found"
        ntable.add_row("Full Name", ndata["n"])
        ntable.add_row("First Name", ndata["nf"])
        ntable.add_row("Middle Name Abbreviated", ndata["nma"])
        ntable.add_row("Middle Name", ndata["nm"])
        ntable.add_row("Last Name", ndata["nl"])
        atable.add_row("Full Address", adata["a"])
        atable.add_row("Address Line", adata["al"])
        atable.add_row("City", adata["ac"])
        atable.add_row("State (or Province)", adata["as"])
        atable.add_row("Nation", adata["an"])
        atable.add_row("Zip Code", adata["az"])
        atable.add_row("Apartment Number", adata["aa"])
        console = Console()
        if table == "-":
            console.print(ntable)
            console.print("\n\n")
            console.print(atable)
            exit()
        elif table == "a":
            console.print(atable)
            exit()
        elif table == "n":
            console.print(ntable)
            exit()
        else:
            raise click.ClickException("Invalid table")
    else:
        rprint("File not found")
        exit()
        
@cli.command()
@click.option("--autoformat", "-a", help="automatically uses the base format (base format in osint format", is_flag=True, default=False)
@click.option("--file", "-f", type=str, help="Name of new file", default="")
def add(autoformat, file):
    """Adds a new data to the osint file"""
    os.system("clear")
    rprint("[bold]Welcome to OSINTer[/]\n\n")
    if file == "":
        file = click.prompt("what file would you like to add to?")
        if not os.path.exists("osint/" + file):
            raise click.ClickException("This file does not exist")
    elif not os.path.exists("osint/" + file):
        raise click.ClickException("This file does not exist")
    fileSplit = []
    divider = "/"
    fileQuery = ""
    fullMiddle = False
    if autoformat == False:
        click.echo("What data would you like to add? (data format) (use osint format to see format names) (make sure to use dividers like '.' or '/')")
        format = click.prompt("Format")
        divider = click.prompt("Divider")
        fileSplit = format.split(divider)
    else: 
        click.echo("What data type are you adding?")
        fileQuery = click.prompt("(a/n/s)")
        if fileQuery == "a":
            fileSplit = ["al", "ac", "as", "an", "az", "aa"]
        elif fileQuery == "n":
            middleQuery = click.prompt("Do you have a full middle name? (y/n)")
            fullMiddle = True if middleQuery == "y" else False
            fullMiddle = False if middleQuery == "n" else True
            if middleQuery not in ["y", "n"]:
                raise click.ClickException("Not a valid option")
            fileSplit = ["n", "nf", "nma", "nm", "nl"]
        elif fileQuery == "s":
            fileSplit = ["fb", "in", "tx", "rd", "li", "tt"]
    for i in fileSplit:
        if i not in formatkeys:
            raise Exception(f"\n\nFormat key '{i}' not found")
    data = click.prompt("Data")
    dsplit = data.split(divider)
    d = dsplit
    for i in range(len(dsplit)):
        ft = fileSplit[i]
        dt = dsplit[i]
        fa = open(f"osint/{file}/address.oie", "r").readlines()
        fn = open(f"osint/{file}/name.oie", "r").readlines()
        fos = open(f"osint/{file}/online/socials.oie", "r").readlines()
        fn.append("\n")
        fa.append("\n")
        fos.append("\n")
        if autoformat == False:
            if ft == "n":
                fn[0] = dt
                open(f"osint/{file}/name.oie", "w").writelines(fn)
            elif ft == "nf":
                fn[1] = dt
                open(f"osint/{file}/name.oie", "w").writelines(fn)
            elif ft == "nma":
                fn[2] = dt
                open(f"osint/{file}/name.oie", "w").writelines(fn)
            elif ft == "nm":
                fn[3] = dt
                open(f"osint/{file}/name.oie", "w").writelines(fn)
            elif ft == "nl":
                fn[4] = dt
                open(f"osint/{file}/name.oie", "w").writelines(fn)
            elif ft == "a":
                fa[0] = dt
                open(f"osint/{file}/address.oie", "w").writelines(fa)
            elif ft == "al":
                fa[1] = dt
                open(f"osint/{file}/address.oie", "w").writelines(fa)
            elif ft == "ac":
                fa[2] = dt
                open(f"osint/{file}/address.oie", "w").writelines(fa)
            elif ft == "as":
                fa[3] = dt
                open(f"osint/{file}/address.oie", "w").writelines(fa)
            elif ft == "an":
                fa[4] = dt
                open(f"osint/{file}/address.oie", "w").writelines(fa)
            elif ft == "az":
                fa[5] = dt
                open(f"osint/{file}/address.oie", "w").writelines(fa)
            elif ft == "aa":
                fa[6] = dt
                open(f"osint/{file}/address.oie", "w").writelines(fa)
        elif autoformat == True:
            if fileQuery == "a":
                if len(d) == 5:
                    d.append("N/A")
                fa = [f"{d[0]}, {d[1]}, {d[2]}, {d[3]}\n",f"{d[0]}\n",f"{d[1]}\n",f"{d[2]}\n",f"{d[3]}\n",f"{d[4]}\n",f"{d[5]}\n"]
                open(f"osint/{file}/address.oie", "w").writelines(fa)
            elif fileQuery == "n":
                if len(d) == 2:
                    fn = [f"{d[0]} {d[1]}\n",f"{d[0]}\n","\n","\n",f"{d[1]}\n"]
                    open(f"osint/{file}/name.oie", "w").writelines(fn)
                elif len(d) == 3:
                    if fullMiddle == True:
                        abm = [*d[1]][0] + "."
                        fn = [f"{d[0]} {d[1]} {d[2]}\n",f"{d[0]}\n",f"{abm}\n",f"{d[1]}\n",f"{d[2]}\n"]
                        open(f"osint/{file}/name.oie", "w").writelines(fn)
                    if fullMiddle == False:
                        fn = [f"{d[0]} {d[1]} {d[2]}\n",f"{d[0]}\n",f"{d[1]}\n","\n",f"{d[2]}\n"]
                        open(f"osint/{file}/name.oie", "w").writelines(fn)
            elif fileQuery == "s":
                fos = [f"{d[0]}\n",f"{d[1]}\n",f"{d[2]}\n",f"{d[3]}\n",f"{d[4]}\n",f"{d[5]}\n"]
                open(f"osint/{file}/online/socials.oie", "w").writelines(fos)
        
@cli.command()
def remove():
    """Removes a specific osint file"""
    os.system("clear")
    rprint("[bold]Welcome to OSINTer[/]\n\n")
    click.echo("Which file would you like to remove?")
    file = click.prompt("(file name)")
    click.echo("\nAre you sure you want to remove this file?")
    con = click.prompt("(y/n)")
    if con == "y":
        os.system("rm -rf osint/" + file)
        click.echo("File removed")
        exit()
    else:
        click.echo("ok, exiting...")
        exit()

@cli.command()
def files():
    """Returns a list of all osint files"""
    os.system("clear")
    rprint("Welcome to OSINTer\n\n")
    click.echo("Files do not include the README.md, or any other setup file\n\n")
    files = os.listdir("osint")
    for i in files:
        if i != "readme.md":
            rprint(i)
    exit()
    
@cli.command()
def format():
    """Returns all types of formating"""
    os.system("clear")
    rprint("[bold]Welcome to OSINTer[/]\n\n")
    rprint("Format keys are the keys that are used to format the data")
    rprint("The following keys describe the data that can be stored\n\n")
    rprint("[bold]Name[/]")
    rprint("  [b]n[/] - Full Name")
    rprint("  [b]nf[/] - First Name")
    rprint("  [b]nma[/] - Middle Name Abbreviated")
    rprint("  [b]nm[/] - Middle Name")
    rprint("  [b]nl[/] - Last Name")
    rprint("\n\n[b]Address[/]")
    rprint("  [b]a[/] - Full Address")
    rprint("  [b]al[/] - Address Line")
    rprint("  [b]ac[/] - City")
    rprint("  [b]as[/] - State (or Province)")
    rprint("  [b]an[/] - Nation (country)")
    rprint("  [b]az[/] - Zip Code")
    rprint("  [b]aa[/] - Apartment Number")
    rprint("\n\n[b]Socials[/]")
    rprint("  [b]s[/] - All Socials")
    rprint("  [b]fb[/] - Facebook")
    rprint("  [b]in[/] - Instagram")
    rprint("  [b]tx[/] - Twitter/X")
    rprint("  [b]rd[/] - Reddit")
    rprint("  [b]li[/] - LinkedIn")
    rprint("  [b]tt[/] - Tiktok")
    rprint("\n\n\n[bold]Autoformats[/]")
    rprint("  [b]a[/] - al/ac/as/an/az(/aa)")
    rprint("  [b]n[/] - nf(/nm)/nl")
    rprint("  [b]s[/] - fb/in/tx/rd/li/tt")
                      
if __name__ == "__main__":
    cli()