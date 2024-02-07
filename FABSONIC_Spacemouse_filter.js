var customGroupVariableName = script.addStringParameter("Group custom variable","Le nom exact du groupe de la custom variable à prendre en compte pour ce filtre.", "Groupe variable name");
var customVariableName = script.addStringParameter("Custom variable","Le nom exact de la custom variable à prendre en compte pour ce filtre.", "Variable name");
var sensitiveVariable = script.addFloatParameter("Sensibilité","Un multiplicateur pour gérer la sensibilité de 0 à 1.",1,0,10);

function filter(inputs) {
    
    var groupVariableName = customGroupVariableName.get().split('');
    groupVariableName[0] = groupVariableName[0].toLowerCase();
    for (var i = 0; i < groupVariableName.length; i++){
        if (groupVariableName[i] == " "){
            groupVariableName[i+1] = groupVariableName[i+1].toUpperCase();
        }
    }
    groupVariableName = groupVariableName.join('').replace(' ','');
    groupVariableName = groupVariableName.replace('-','_');
    groupVariableName = groupVariableName.replace('\'','_');
    groupVariableName = groupVariableName.replace('\/','_');
    var variableName = customVariableName.get().split('');
    variableName[0] = variableName[0].toLowerCase();
    for (var i = 0; i < variableName.length; i++){
        if (variableName[i] == " "){
            variableName[i+1] = variableName[i+1].toUpperCase();
        }
    }
    variableName = variableName.join('').replace(' ','');
    variableName = variableName.replace('-','_');
    variableName = variableName.replace('\'','_');
    variableName = variableName.replace('\/','_');
	var modifiedValue = parseFloat(root.customVariables[groupVariableName].variables[variableName][variableName].get());
//------------
    script.log('Inputs 0 = ' + inputs[0]);
    script.log('sensitiveVariable = ' + sensitiveVariable);
    script.log('modifiedValue = ' + modifiedValue);

    modifiedValue = modifiedValue + (inputs[0] * sensitiveVariable.get());
    var result = [modifiedValue];
	return result;
}