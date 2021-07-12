//
//  HomeModel.swift
//  GrubGridAppStore
//
//  Created by Bennett Desmond on 7/10/21.
//

import UIKit

protocol HomeModelDelegate {
    func itemsDownloaded(recipes:[Recipe])
}

class HomeModel: NSObject {
    
    var delegate:HomeModelDelegate?
    func getItems() {
        // Hit the web service Url
        let serviceUrl = "https://bennettadesmond.com/service.php"
        
        // Download the json data
        let url = URL(string: serviceUrl)
        
        if let url = url {
            
            //Create a URL Session
            let session = URLSession(configuration: .default)
            let task = session.dataTask(with: url, completionHandler:
                    {(data, response, error) in
                    if error == nil {
                        //Succeed
                        
                        //Call parse json function on the data
                        self.parseJSON(data!)
                    }
                    else {
                        //Error occurred
                    }
                })
            
            task.resume()
        }
        
        // Parse it out inot Location structs
        
        // Notify the view controller and pass the data back
    }
    
    func parseJSON(_ data:Data) {
            
        var recipeArray = [Recipe]()
        
        do {
            let jsonArray = try JSONSerialization.jsonObject(with: data, options: []) as! [Any]
            for jsonResult in jsonArray {
                let jsonDict = jsonResult as! [String:String]
                
                /*let recipe = Recipe(name: jsonDict["name"]!, recipe_id: Int(jsonDict["recipe_id"] ?? 0)!, minutes: jsonDict["minutes"]!, nutrition: jsonDict["nutrition"]!, n_steps: jsonDict["n_steps"]!, steps: jsonDict["steps"]!, description: jsonDict["description"]!, ingredients: jsonDict["ingredients"]!, index: jsonDict["index"]!)*/
                
                //recipeArray.append(recipe)
            }
            delegate?.itemsDownloaded(recipes: recipeArray)
        } catch {
            
            print("There was an error")
        }
    
    }
    
}
