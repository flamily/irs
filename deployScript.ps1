$resourceGroupName = "travisTest"
$templatePath = "C:\Users\david\Documents\ictd_test\templates\appService.Json"

New-AzureRmResourceGroup -Name $resourceGroupName -Location "Australia East" -Verbose -Force
New-AzureRmResourceGroupDeployment -ResourceGroupName $resourceGroup -TemplateFile $templatePath 