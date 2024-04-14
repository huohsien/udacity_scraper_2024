var pageHeight = 0;
function findHighestNode(nodesList) {
    for (var i = nodesList.length - 1; i >= 0; i--) {
        if (nodesList[i].scrollHeight && nodesList[i].clientHeight) {
            var elHeight = Math.max(nodesList[i].scrollHeight, nodesList[i].clientHeight);
            if (nodesList[i].scrollHeight>nodesList[i].clientHeight) {
                console.log("node: ",nodesList[i],"scrollHeight: ",nodesList[i].scrollHeight);
            }
            pageHeight = Math.max(elHeight, pageHeight);
        }
        if (nodesList[i].childNodes.length) findHighestNode(nodesList[i].childNodes);
    }
}
findHighestNode(document.documentElement.childNodes);
return pageHeight;



function findHighestNode(nodesList) {    for (var i = nodesList.length - 1; i >= 0; i--) {        if (nodesList[i].scrollHeight && nodesList[i].clientHeight) {            var elHeight = Math.max(nodesList[i].scrollHeight, nodesList[i].clientHeight);            if (nodesList[i].scrollHeight>nodesList[i].clientHeight) {                console.log("node: ",nodesList[i],"scrollHeight: ",nodesList[i].scrollHeight);            }            pageHeight = Math.max(elHeight, pageHeight);        }        if (nodesList[i].childNodes.length) findHighestNode(nodesList[i].childNodes);    }}