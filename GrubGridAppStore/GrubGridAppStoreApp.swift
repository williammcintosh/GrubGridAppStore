//
//  GrubGridAppStoreApp.swift
//  GrubGridAppStore
//
//  Created by Will McIntosh on 6/23/21.
//

import SwiftUI

@main
struct GrubGridAppStoreApp: App {
    var body: some Scene {
        WindowGroup {
            TabView {
                //This below will create the frosted view on top of the notch for ScrollView
                NavigationView {
                    ContentView()
                }
                //ContentView()
            }
            .tabItem {
                Image(systemName: "airplane.circle.fill")
                Text("Discover")
            }
        }
    }
}
