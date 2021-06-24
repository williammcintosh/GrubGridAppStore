//
//  ContentView.swift
//  GrubGridAppStore
//
//  Created by Will McIntosh on 6/23/21.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        //Change this to a ScrollView to scroll
        //Scroll View {
        VStack {
            Text("GrubGrid")
                .font(.largeTitle)
            Text("A flexible meal-planning app")
                .foregroundColor(.secondary)
            Image("GrubGridIcon")
                .resizable()
                .scaledToFit()
            Text("This is some text")
                .padding(.top)
            //Hello
            
            //This works
        }
        
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        Group {
            ContentView()
        }
    }
}
