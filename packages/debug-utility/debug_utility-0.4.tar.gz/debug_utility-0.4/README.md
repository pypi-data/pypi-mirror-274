# utility
Utility commonly used for debug
        
Setup Required inputs
# required inputs "ri" for utility_class.load_file_as_string(ri)
        ri = { 
            "full_path_file_name": None,
        }
      

# required inputs "ri" for utility_class.load_configuration_file(ri)
    ri = {
             "configuration_full_path_file_name": None,
         }

# required inputs for debug_class()
Pass a dictionary as an argument to print out the contents

    debug_utility.debug_file.debug_class({
        "title": "execute()",
        "df": df,
    }, True)