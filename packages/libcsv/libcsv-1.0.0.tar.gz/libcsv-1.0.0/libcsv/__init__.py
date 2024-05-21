def openTable(tableName):
    try:
        with open(tableName) as csvTable:
            options = {
                "name": tableName,
                "rows": 0,
                "columns": 0,
                "contents": []
            }
            for column in csvTable.readlines():
                line = []
                options["rows"] += 1
                for row in column.split(";" or "; "):
                    if len(options["contents"]) == 0:
                        options["columns"] += 1
                    line.insert(len(line), row.strip("\n"))
                options["contents"].insert(len(options["contents"]), line)
            return options
                
            
    except FileNotFoundError as e:
        raise TableDoesntExist("CSV table " + tableName + " doesn't exist.")
        
def writeTable(tableName, options):
    with open(tableName, "w") as csvTable:
        writeOptions = {
            "name": options["name"],
            "rows": options["rows"],
            "columns": options["columns"],
            "contents": options["contents"]
        }
        lines=""
        for value in writeOptions["contents"]:
            for i, value2 in enumerate(value):
                if i < len(value)-1:
                    lines = lines + str(value2) + ";"
                else:
                    lines = lines + str(value2)
                
            lines = lines + "\n"
                
        csvTable.write(str(lines))
        return lines
        
class TableDoesntExist(Exception):
    def __init__(self, message):
        super().__init__(message)
