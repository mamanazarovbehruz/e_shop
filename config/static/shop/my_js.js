async function check(val){
 let ress = await fetch("https://ksjsdkfjksd")
 .then(response => {
    return response
 })
 .catch(err => {
    return JSON.stringify(err)
 })

 render(ress)
 return ress
}

function render (ressss){
    
}