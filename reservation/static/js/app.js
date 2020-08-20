if (document.URL === "http://127.0.0.1:7500/reservation/hotele/dodaj") {
let my_continents = document.querySelector('#id_continent')
let my_countries = document.querySelector('#id_country')
let my_regions = document.querySelector('#id_region')

    my_continents.addEventListener("click", function (){
        let my_val = my_continents.options[my_continents.selectedIndex]
        const ADDRESS='http://127.0.0.1:7500/reservation/rest/get_countries/?continent_id=' + my_val.value
        console.log(ADDRESS)
        fetch(`${ADDRESS}`, {method:"GET"}).then(response=>{
        //Promise
        if(response.status===200){  //response.isOk
            return response.text()
        }
        }).then(html=>{
            my_countries.innerHTML = html
            console.log(html)
        }).catch(err=>{
        alert(err)
        })
    })
    my_countries.addEventListener("click", function (){
        let my_val = my_countries.options[my_countries.selectedIndex]
        const ADDRESS='http://127.0.0.1:7500/reservation/rest/get_regions/?country_id=' + my_val.value
        fetch(`${ADDRESS}`, {method:"GET"}).then(response=>{
        //Promise
        if(response.status===200){  //response.isOk
            return response.text()
        }
        }).then(html=>{
            my_regions.innerHTML = html
            console.log(html)
        }).catch(err=>{
        alert(err)
        })
    })
}



// function get_cars(event){
//     var id = this.dataset.id;
//     var address = "/rest/get_cars/";
//     var data = {'type_id':id};
//     $.get(address, data, function (data, status) {
//         alert(data);
//         $("#cars").html(data);
//     });
// }
//
//
// $(document).ready(function () {
//     var types_li = $(".type");
//     types_li.click(get_cars);
//
// });




