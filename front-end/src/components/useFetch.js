import { useState, useEffect } from "react"

const useFetch = (url, id) => {

    const[data, setData ] = useState([]);
    
    useEffect(() => {

        fetch(url + id, {
          method : 'GET',
          headers: {
            'Content-Type' : 'application/json'
          }
        })
        .then(resp => resp.json())
        .then(resp => setData(resp))
        .catch(error => console.log(error))
      }, [url, id]);
      console.log(data)
    return({data});

}

export default useFetch