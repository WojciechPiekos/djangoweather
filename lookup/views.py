from django.shortcuts import render

def home(request):
    import requests

    def response(zipcode):
        try:
            api_request = requests.get(f"https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode={zipcode}&distance=25&API_KEY=8E56A117-9F3B-4F3F-AD00-B87CE2217EA0")
            api_data = api_request.json()
        except Exception as e:
            api_data = "Error..."

        if api_data:

            if api_data[0]["Category"]["Name"] == "Good":
                category_description = "Air quality is satisfactory, and air pollution poses little or no risk."
                category_color = "good"
            
            elif api_data[0]["Category"]["Name"] == "Moderate":
                category_description = """Air quality is acceptable. However, there may be a risk for some people,
                                        particularly those who are unusually sensitive to air pollution."""
                category_color = "moderate"
            
            elif api_data[0]["Category"]["Name"] == "Unhealthy for Sensitive Groups":
                category_description = """Members of sensitive groups may experience health effects. 
                                            The general public is less likely to be affected."""
                category_color = "usg"
            
            elif api_data[0]["Category"]["Name"] == "Unhealthy":
                category_description = """Some members of the general public may experience health effects;
                                            members of sensitive groups may experience more serious health effects."""
                category_color = "unhealthy"
            
            elif api_data[0]["Category"]["Name"] == "Very Unhealthy":
                category_description = "Health alert: The risk of health effects is increased for everyone."
                category_color = "very-unhealthy"
            
            elif api_data[0]["Category"]["Name"] == "Hazardous":
                category_description = "Health warning of emergency conditions: everyone is more likely to be affected."
                category_color = "hazardous"

            return {'category_description' : category_description,
                    'api' : api_data,
                    'category_color' : category_color
                    }
        else:
            api_data = ""
    
    
    if request.method == "POST":
        zipcode = request.POST['zipcode']
        data = response(zipcode=zipcode)
        if data:
            return render(request,'home_page.html',{'category_description' : data['category_description'],
                                                'api' : data['api'],
                                                'category_color' : data['category_color']
                                                })
        else:
            return render(request,'home_page.html',{})
    
    else:
        data = response(zipcode=89129)
        return render(request,'home_page.html',{'category_description' : data['category_description'],
                                                'api' : data['api'],
                                                'category_color' : data['category_color']
                                                })

def about(request):
    return render(request,'about.html',{})