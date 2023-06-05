function predict() {
    // While predicting
    document.getElementById("label").innerHTML = "Predicting..."

    const text = document.getElementById("input");
    const threshold = 0.9;
    toxicity.load(threshold).then(model => {
        const sentences = [text.value];
        model.classify(sentences).then(predictions => {
            console.log(predictions);
            var checker = 0;
            for(i=0; i<7; i++){
                if(predictions[i].results[0].match){
                    checker = 1;
                    console.log(predictions[i].label + 
                                " was found with probability of " + 
                                predictions[i].results[0].probabilities[1]);                
                }  
            }
            if(checker > 0){
                document.getElementById("label").innerHTML = "The output is: "
                document.getElementById("answer").innerHTML = "TOXIC!";
                document.getElementById("answer").style.color = "red";
            } else {
                document.getElementById("label").innerHTML = " The output is: "
                document.getElementById("answer").innerHTML = "NOT TOXIC";
                document.getElementById("answer").style.color = "green";
            }
        });
    });
}

