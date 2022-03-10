import {useEffect, useRef } from "react";


const useInterval = (callback, delay) => {
    const savedCallBack = useRef();
    console.log("called")
    

    useEffect(() => {
        savedCallBack.current = callback;
    }, [callback]);

    useEffect(() => {
        function tick() {
            savedCallBack.current();
            console.log("this is working")
        }
        if (delay !== null) {
            let id = setInterval(tick, delay);
            return () => {
                console.log("cleared!")
            clearInterval(id);
            }
        }
    }, [delay])
}

export default useInterval