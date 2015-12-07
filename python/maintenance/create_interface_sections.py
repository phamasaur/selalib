# coding: utf8
"""
Create interface sections for all modules (and programs?) in a Fortran library.

Modules required
----------------
  * Built-in  : os, sys, argparse
  * Library   : maintenance_tools, sll2py

"""
#
# Author: Yaman Güçlü, Oct 2015 - IPP Garching
#
# Last revision: 04 Dec 2015
#
from __future__ import print_function

__all__ = ['create_interface_sections','main']
__docformat__ = 'reStructuredText'

#==============================================================================
# PARAMETERS.. CHANGE THIS
#==============================================================================

ignored_symbols = [ \
        'mudpack_curvilinear_cof',
        'mudpack_curvilinear_cofcr',
        'mudpack_curvilinear_bndcr',
        'sol',
        'mulku',
        ]

permissive_modules = ['sll_m_hdf5_io_parallel']

forced_public_symbols = [ \
        'sll_new',
        'sll_create',
        'sll_solve',
        'sll_delete',
        'operator(*)',
        ]

def ignore_dir( d ):
    """ Return True if subdirectory should be ignored.
    """
    non_source_dirs = ['bin','CMakeFiles','doc','include','modules','Testing']
    useless_subdirs = ['ctags','no_gfortran']
    ignore = (d in non_source_dirs) or (d in useless_subdirs)
    return ignore

def select_file( f ):
    """ Return True if filename should be selected for processing.
    """
    is_preprocessed_fortran = f.endswith( '.f90' )
    return is_preprocessed_fortran

#==============================================================================
# UTILITY FUNCTIONS (needed for Python2, as 'maintenance_tools' is for Python3)
#==============================================================================

def find_module_def( filename ):
    mod_def_list = []
    with open( filename, 'r' ) as f:
        for line in f:
            spl = line.partition( '!' )[0].split()
            if len( spl ) > 1:
                if spl[0] == 'module' and spl[1] != 'procedure':
                    mod_def_list.append( spl[1] )
    return mod_def_list

def find_program_name( filename ):
    program_list = []
    with open( filename, 'r' ) as f:
        for line in f:
            spl = line.partition( '!' )[0].split()
            if len( spl ) > 1:
                if spl[0] == 'program':
                    program_list.append( spl[1] )
    return program_list

def contains_exactly_1_module( filepath, verbose=False ):
    """ Determine if only one module is present, otherwise ignore file.
    """
    num_mods = len( find_module_def( filepath ) )
    if len( find_program_name( filepath ) ) > 0:
        skip_file = True
        if verbose: print( "WARNING: Fortran program. ", end='' )
    elif num_mods > 1:
        skip_file = True
        if verbose: print( "WARNING: multiple module definitions. ", end='' )
    elif num_mods == 0:
        skip_file = True
        if verbose: print( "WARNING: no modules or programs in file. ", end='' )
    else:
        skip_file = False
    if skip_file:
        if verbose: print( "Skipping file '%s'" % filepath )
    return (not skip_file)

#==============================================================================
# Overwrite instance methods (special cases)
#==============================================================================

def add_exported_symbols_permissive( self, *symbols ):
    for s in symbols:
        if not self.defines_symbol( s ):
            mod_name, mod_obj = self.find_symbol_def( s )
            if mod_name:
                print( "WARNING processing file '%s':" % self.filepath )
                print( "  symbol '%s' is imported but not defined here" % s )
                print( "  original definition in module '%s'" % mod_name )
            else:
                print( "ERROR processing file '%s':" % self.filepath )
                print( "  symbol '%' is neither defined nor imported here" % s )
                raise SystemExit()
        self._exported_symbols.add( s )

def make_modules_permissive( *modules ):
    from types import MethodType
    for m in modules:
        if m.name in permissive_modules:
            m.add_exported_symbols = \
                    MethodType( add_exported_symbols_permissive, m )

#==============================================================================
# HELPER FUNCTION
#==============================================================================

def parse_file_and_create_unit( fpath, modules, programs ):

    from sll2py.fparser.api      import parse
    from sll2py.fortran_module   import NewFortranModule
    from sll2py.fortran_program  import FortranProgram

    im = len(  modules )
    ip = len( programs )

    mod_names = find_module_def  ( fpath )
    prg_names = find_program_name( fpath )

    if len( mod_names ) == 1 and len( prg_names ) == 0:
        # Create fparser module object
        tree = parse( fpath, analyze=False )
        fmod = tree.content[0]
        # Create 'my' module object and store it in dictionary
        print("  - read module  %3d: %s" % (im+1, fmod.name ) );  im += 1
        modules.append( NewFortranModule( fpath, fmod ) )
    elif len( mod_names ) == 0 and len( prg_names ) == 1:
        # Create fparser program object
        tree = parse( fpath, analyze=False )
        fprg = tree.content[0]
        # Create 'my' program object and store it in dictionary
        print("  - read program %3d: %s" % (ip+1, fprg.name ) );  ip += 1
        programs.append( FortranProgram( fpath, fprg ) )
    elif len( mod_names ) == 0 and len( prg_names ) == 0:
        print( "ERROR: No modules or programs in file %s" % fpath )
        raise SystemExit()
    else:
        print( "ERROR: Multiple modules/programs in file %s" % fpath )
        if mod_names: print( "  Modules  = [%s]" % ', '.join( mod_names ) )
        if prg_names: print( "  Programs = [%s]" % ', '.join( prg_names ) )
        raise SystemExit()

#==============================================================================
# MAIN FUNCTION
#==============================================================================

def create_interface_sections( root, src='src', interfaces='src/interfaces' ):
    """
    Create interface sections for all modules (and programs?)
    in a Fortran library.

    Parameters
    ----------
    root : str
      Relative path to root of directory tree

    """
    import os
    from maintenance_tools        import recursive_file_search
    from sll2py.fortran_external  import external_modules, find_external_library

    print( "================================================================" )
    print( "[1] Processing library modules and programs")
    print( "================================================================" )
    src_modules  = []
    src_programs = []

    # Walk library tree and store FortranModule (or FortranProgram) objects
    src_root = os.path.join( root, src )
    for fpath in recursive_file_search( src_root, ignore_dir, select_file ):
        if interfaces in fpath:
            print( "WARNING: Interface. Skipping file %s" % fpath )
            continue
        parse_file_and_create_unit( fpath, src_modules, src_programs )

    # Additional source directory (ad-hoc)
    src_root = os.path.join( root, 'external/burkardt' )
    for fpath in recursive_file_search( src_root, ignore_dir, select_file ):
        parse_file_and_create_unit( fpath, src_modules, src_programs )

    # Interface modules
    print( "================================================================" )
    print( "[2] Processing interface modules and programs" )
    print( "================================================================" )
    int_modules  = []
    int_programs = []
    int_root     = os.path.join( root, interfaces )
    for fpath in recursive_file_search( int_root, ignore_dir, select_file ):
        parse_file_and_create_unit( fpath, int_modules, int_programs )

    # List with all the modules
    all_modules = []
    all_modules.extend( src_modules )
    all_modules.extend( int_modules )

    # Test: no modules with same name
    from maintenance_tools import all_different, get_repetition_count
    module_names = [mmod.name for mmod in all_modules]
    if not all_different( *module_names ):
        print("ERROR: repeated module names:")
        for item,count in get_repetition_count( module_names ):
            print("  . %d occurrences for module '%s'" % (count,item) )
        raise SystemExit()

    print( "================================================================" )
    print( "[3] Library modules/programs: Link against used modules" )
    print( "================================================================" )
    # Link library modules/programs against used modules, creating a graph
    for i,mmod in enumerate( src_modules ):
        print("  - link module %3d: %s" % (i+1,mmod.name) )
        mmod.link_used_modules( all_modules, externals=external_modules )

    # TODO: what about interface programs?
    print( "----------------------------------------------------------------" )
    for i,mprg in enumerate( src_programs ):
        print("  - link program %3d: %s" % (i+1,mprg.name) )
        mprg.link_used_modules( all_modules, externals=external_modules )

    print( "================================================================" )
    print( "[4] Library modules/programs: Search symbols in used modules" )
    print( "================================================================" )
    # Update use statements (recursively search symbols in used modules)
    for i,mmod in enumerate( src_modules ):
        print("  - update module %3d: %s" % (i+1,mmod.name) )
        mmod.update_use_statements( find_external_library, ignored_symbols )

    print( "----------------------------------------------------------------" )
    for i,mprg in enumerate( src_programs ):
        print("  - update program %3d: %s" % (i+1,mprg.name) )
        mprg.update_use_statements( find_external_library, ignored_symbols )

    print( "================================================================" )
    print( "[5] Library modules/programs: Cleanup use statements" )
    print( "================================================================" )
    # Cleanup use statements (remove duplicate symbols and useless modules)
    for i,mmod in enumerate( src_modules ):
        print("  - cleanup module %3d: %s" % (i+1,mmod.name) )
        mmod.cleanup_use_statements()

    print( "----------------------------------------------------------------" )
    for i,mprg in enumerate( src_programs ):
        print("  - cleanup program %3d: %s" % (i+1,mprg.name) )
        mprg.cleanup_use_statements()

    print( "================================================================" )
    print( "[6] Library modules/programs: Scatter imported symbols" )
    print( "================================================================" )

    # Some modules must be made permissive
    make_modules_permissive( *src_modules )

    for i,mmod in enumerate( src_modules ):
        print("  - scatter from module %3d: %s" % (i+1,mmod.name) )
        mmod.scatter_imported_symbols()

    print( "----------------------------------------------------------------" )
    for i,mprg in enumerate( src_programs ):
        print("  - scatter from program %3d: %s" % (i+1,mprg.name) )
        mprg.scatter_imported_symbols()

    # Force some symbols to be always public
    for s in forced_public_symbols:
        print( "----------------------------------------------------------------" )
        for i,mmod in enumerate( src_modules ):
            if mmod.defines_symbol( s ) and (s not in mmod.exported_symbols):
                print("  - set '%s' public in module %3d: %s" % (s,i+1,mmod.name) )
                mmod.add_exported_symbols( s )

    print( "================================================================" )
    print( "[7] Library modules/programs: Generate interface sections" )
    print( "================================================================" )
    for i,mmod in enumerate( src_modules ):
        print("  - interface for module %3d: %s" % (i+1,mmod.name) )
        interface = mmod.generate_interface_section()
        if interface:
            filepath  = mmod.filepath[:-4] + '-interface.txt'
            with open( filepath, 'w' ) as f:
                print( interface, file=f )

    print( "----------------------------------------------------------------" )
    for i,mprg in enumerate( src_programs ):
        print("  - interface for program %3d: %s" % (i+1,mprg.name) )
        interface = mprg.generate_interface_section()
        filepath  = mprg.filepath[:-4] + '-interface.txt'
        with open( filepath, 'w' ) as f:
            print( interface, file=f )

    # DONE
    print( "DONE" )

    # Return dictionary with local variables (useful for interactive work)
    return locals()

#==============================================================================
# PARSER
#==============================================================================

def parse_input():

  import argparse, sys

  parser = argparse.ArgumentParser (
      prog        = 'python '+ sys.argv[0],
      description = 'Create interface sections for all modules (and programs?)'
                    ' in a Fortran library.',
      epilog      = ' ',
      formatter_class = argparse.ArgumentDefaultsHelpFormatter,
      )

  parser.add_argument( metavar = 'ROOT',
                       dest    = 'root',
                       help    = 'relative path of the root directory' )

  return parser.parse_args()

#==============================================================================
# SCRIPT FUNCTIONALITY
#==============================================================================

def main():

    # Parse input arguments
    print('')
    args = parse_input()
    print(args)
    print('')

    # Walk directory tree and create interface sections
    create_interface_sections( args.root )

#------------------------------------------------------------------------------
if __name__ == '__main__':
    # Run as main program
    main()

