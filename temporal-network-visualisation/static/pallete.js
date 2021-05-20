// Colours will be used for for the vertices
const COLOURS = ["#DF72C6", "#08B5F4", "#D5AB36", "#1F399B", "#1AB0D7", "#583974",
                    "#FF08D6","#26145D","#7FE902","#9DFFCF","#F8A781","#FA6455","#7CD291",
                    "#DCE51D", "#328BFE","#9EBBD6","#CCE3A6","#B6CA34","#E59776","#000000"]
                    
function randomNumber(maxNum) {
    return Math.floor(Math.random() * maxNum)
}

function randomColour(colours, totalColours) {
    return colours[randomNumber(totalColours)]
}