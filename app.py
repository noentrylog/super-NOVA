from fasthtml.common import *
import json
from typing import Dict, List, Any
import google.generativeai as genai
import re

# Create FastHTML app
app, rt = fast_app()

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyC2pvdNtfXN45MeE49B4eomFsv_q50J76Q"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Nova Car Solutions - Business Data
NOVA_IDENTITY = {
    "name": "Nova",
    "tagline": "Your Trusted Partner in Finding the Perfect Car",
    "vision": "To be your trusted partner in finding the perfect car for you.",
    "mission": "Delivering the best, most personalized solutions to match every need."
}

# Car categories and data
CAR_CATEGORIES = {
    "hatchback": {"name": "Hatchback", "icon": "🚗", "capacity": "2-5 passengers"},
    "sedan": {"name": "Sedan", "icon": "🚙", "capacity": "4-5 passengers"},
    "suv": {"name": "SUV", "icon": "🚛", "capacity": "5-7 passengers"},
    "van": {"name": "Van", "icon": "🚐", "capacity": "7-9 passengers"},
    "luxury": {"name": "Luxury", "icon": "🏎️", "capacity": "2-5 passengers"}
}

ENERGY_TYPES = {
    "electric": {"name": "Electric", "icon": "⚡", "description": "Zero emissions, eco-friendly"},
    "hybrid": {"name": "Hybrid", "icon": "🔄", "description": "Best of both worlds"},
    "fuel": {"name": "Fuel", "icon": "⛽", "description": "Traditional reliability"}
}

# Pricing tiers
PRICING_TIERS = {
    "basic": {"name": "Basic", "price": "$29/day", "features": ["Standard car", "Basic insurance", "24/7 support"]},
    "premium": {"name": "Premium", "price": "$49/day", "features": ["Premium car", "Full insurance", "Priority support", "Free maintenance"]},
    "luxury": {"name": "Luxury", "price": "$89/day", "features": ["Luxury car", "Premium insurance", "Concierge service", "All-inclusive maintenance"]}
}

# AI Search Functions
def parse_customer_request(user_input: str) -> Dict[str, Any]:
    """Parse customer's natural language request using Gemini AI"""
    try:
        prompt = f"""
        You are a car rental assistant for Nova Car Solutions. Parse the following customer request and extract key information.
        
        Customer request: "{user_input}"
        
        Extract and return ONLY a JSON object with these fields:
        {{
            "passengers": number (1-2, 3-4, 5-6, 7+),
            "car_type": string (hatchback, sedan, suv, van, luxury),
            "energy_type": string (electric, hybrid, fuel),
            "style": string (family, sport, luxury, practical),
            "duration": number (days),
            "location": string (city/country),
            "travel_purpose": string (daily, weekend, long, cargo)
        }}
        
        Rules:
        - If passenger count not specified, infer from context (family trip = 4, business = 2, etc.)
        - If car type not specified, infer from passenger count and context
        - If energy type not specified, default to "fuel"
        - If duration not specified, default to 1
        - If location not specified, default to "Not specified"
        - Map luxury/expensive requests to "luxury" style
        - Map family/group requests to "family" style
        """
        
        response = model.generate_content(prompt)
        # Clean the response text to handle potential formatting issues
        response_text = response.text.strip()
        # Remove any markdown formatting if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        result = json.loads(response_text.strip())
        return result
    except Exception as e:
        print(f"AI parsing error: {e}")  # Debug output
        # Fallback parsing with better logic
        user_lower = user_input.lower()
        
        # Simple keyword-based parsing as fallback
        passengers = "3-4"
        if any(word in user_lower for word in ["7", "seven", "large", "big"]):
            passengers = "7+"
        elif any(word in user_lower for word in ["1", "one", "2", "two", "couple"]):
            passengers = "1-2"
        elif any(word in user_lower for word in ["5", "five", "6", "six"]):
            passengers = "5-6"
        
        car_type = "sedan"
        if any(word in user_lower for word in ["suv", "sport utility"]):
            car_type = "suv"
        elif any(word in user_lower for word in ["van", "minivan"]):
            car_type = "van"
        elif any(word in user_lower for word in ["hatchback", "hatch"]):
            car_type = "hatchback"
        elif any(word in user_lower for word in ["luxury", "luxurious", "premium", "expensive"]):
            car_type = "luxury"
        
        energy_type = "fuel"
        if any(word in user_lower for word in ["electric", "ev", "battery"]):
            energy_type = "electric"
        elif any(word in user_lower for word in ["hybrid"]):
            energy_type = "hybrid"
        
        style = "practical"
        if any(word in user_lower for word in ["luxury", "luxurious", "premium"]):
            style = "luxury"
        elif any(word in user_lower for word in ["family", "kids", "children"]):
            style = "family"
        elif any(word in user_lower for word in ["sport", "sports", "fast", "performance"]):
            style = "sport"
        
        duration = 1
        for word in user_lower.split():
            if word.isdigit():
                duration = int(word)
                break
        
        location = "Not specified"
        # Simple location detection
        if "bangkok" in user_lower:
            location = "Bangkok"
        elif any(word in user_lower for word in ["beach", "coast", "seaside"]):
            location = "Beach"
        elif any(word in user_lower for word in ["city", "urban", "downtown"]):
            location = "City"
        
        return {
            "passengers": passengers,
            "car_type": car_type,
            "energy_type": energy_type,
            "style": style,
            "duration": duration,
            "location": location,
            "travel_purpose": "weekend"
        }

def generate_ai_recommendations(parsed_request: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate car recommendations based on parsed request"""
    passengers = parsed_request.get("passengers", "3-4")
    car_type = parsed_request.get("car_type", "sedan")
    energy_type = parsed_request.get("energy_type", "fuel")
    style = parsed_request.get("style", "practical")
    duration = parsed_request.get("duration", 1)
    location = parsed_request.get("location", "Not specified")
    
    recommendations = []
    
    # Generate 3-5 curated options based on the parsed request
    if car_type == "suv" and style == "luxury":
        recommendations.append({
            "id": "luxury-suv-1",
            "name": "Nova Luxury Explorer",
            "model": "Premium SUV",
            "type": "Luxury SUV",
            "energy": energy_type.title(),
            "passengers": "7",
            "price": f"${89 * duration}/total",
            "daily_price": "$89/day",
            "features": ["Premium leather seats", "Advanced safety systems", "Entertainment system", "Climate control"],
            "match_score": "98%",
            "image": "🚛",
            "insurance_options": ["Premium coverage (+$15/day)", "Basic coverage (included)"],
            "add_ons": ["GPS Navigation (+$5/day)", "Child seats (+$10/day)", "Driver service (+$50/day)"]
        })
    
    if car_type == "suv":
        recommendations.append({
            "id": "suv-standard",
            "name": "Nova Adventure",
            "model": "Standard SUV",
            "type": "SUV",
            "energy": energy_type.title(),
            "passengers": "7",
            "price": f"${45 * duration}/total",
            "daily_price": "$45/day",
            "features": ["Spacious interior", "All-wheel drive", "Cargo space", "Roof rails"],
            "match_score": "92%",
            "image": "🚙",
            "insurance_options": ["Full coverage (+$10/day)", "Basic coverage (included)"],
            "add_ons": ["GPS Navigation (+$5/day)", "Child seats (+$10/day)", "Cargo box (+$15/day)"]
        })
    
    if car_type == "van":
        recommendations.append({
            "id": "van-family",
            "name": "Nova Family Van",
            "model": "Family Van",
            "type": "Van",
            "energy": energy_type.title(),
            "passengers": "8",
            "price": f"${55 * duration}/total",
            "daily_price": "$55/day",
            "features": ["Maximum seating", "Sliding doors", "Cargo space", "Family-friendly"],
            "match_score": "95%",
            "image": "🚐",
            "insurance_options": ["Family coverage (+$12/day)", "Basic coverage (included)"],
            "add_ons": ["Multiple child seats (+$15/day)", "GPS Navigation (+$5/day)", "Entertainment system (+$20/day)"]
        })
    
    # Always include a luxury option for luxury requests
    if style == "luxury":
        recommendations.append({
            "id": "luxury-sedan",
            "name": "Nova Premium Elite",
            "model": "Luxury Sedan",
            "type": "Luxury",
            "energy": energy_type.title(),
            "passengers": "4",
            "price": f"${89 * duration}/total",
            "daily_price": "$89/day",
            "features": ["Premium amenities", "Concierge service", "White-glove treatment", "Luxury interior"],
            "match_score": "96%",
            "image": "🏎️",
            "insurance_options": ["Premium coverage (+$20/day)", "Full coverage (included)"],
            "add_ons": ["Personal driver (+$100/day)", "Airport pickup (+$25)", "Luxury amenities (+$30/day)"]
        })
    
    # Add a practical option
    recommendations.append({
        "id": "practical-sedan",
        "name": "Nova Reliable",
        "model": "Standard Sedan",
        "type": "Sedan",
        "energy": energy_type.title(),
        "passengers": "5",
        "price": f"${35 * duration}/total",
        "daily_price": "$35/day",
        "features": ["Reliable performance", "Good fuel economy", "Comfortable seating", "Standard features"],
        "match_score": "88%",
        "image": "🚗",
        "insurance_options": ["Full coverage (+$8/day)", "Basic coverage (included)"],
        "add_ons": ["GPS Navigation (+$5/day)", "Child seat (+$10/day)", "Extra driver (+$5/day)"]
    })
    
    return recommendations[:5]  # Return max 5 recommendations

def generate_chatbot_response(parsed_request: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> str:
    """Generate chatbot follow-up questions based on request and recommendations"""
    car_type = parsed_request.get("car_type", "sedan")
    passengers = parsed_request.get("passengers", "3-4")
    
    if car_type == "suv" or car_type == "van":
        return f"Great choices for {passengers} passengers! Would you like a driver service or self-drive? Also, do you need child seats or any cargo add-ons for your trip?"
    elif car_type == "luxury":
        return f"Perfect! For your luxury {car_type}, would you like our personal driver service or prefer to drive yourself? We can also arrange airport pickup and luxury amenities."
    else:
        return f"Excellent selection! For your {car_type}, would you like to add GPS navigation, child seats, or an additional driver to your rental?"

def create_header():
    return Header(
        Nav(
            A("Nova", href="/", cls="brand"),
            Ul(
                Li(A("Find Your Car", href="/car-finder")),
                Li(A("AI Demo", href="/ai-demo")),
                Li(A("Services", href="/services")),
                Li(A("Pricing", href="/pricing")),
                Li(A("About", href="/about")),
                Li(A("Contact", href="/contact"))
            )
        )
    )

def create_footer():
    return Footer(
        Container(
            Div(
                Div(
                    H3("Nova"),
                    P("Your trusted partner in finding the perfect car for you."),
                    P("© 2024 Nova Car Solutions. All rights reserved.")
                ),
                Div(
                    H4("Services"),
                    Ul(
                        Li(A("Car Rental", href="/rental")),
                        Li(A("Car Sales", href="/sales")),
                        Li(A("Maintenance", href="/maintenance")),
                        Li(A("Insurance", href="/insurance"))
                    )
                ),
                Div(
                    H4("Contact"),
                    P("📞 +1 (555) NOVA-CAR"),
                    P("✉️ hello@nova-cars.com"),
                    P("📍 123 Auto Street, Car City")
                )
            ),
            style="display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 2rem; margin-top: 2rem;"
        )
    )

@rt("/")
def index():
    return Html(
        Head(
            Title(f"{NOVA_IDENTITY['name']} - {NOVA_IDENTITY['tagline']}"),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"),
            Style("""
                .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 4rem 0; text-align: center; }
                .hero h1 { font-size: 3rem; margin-bottom: 1rem; }
                .hero p { font-size: 1.2rem; opacity: 0.9; margin-bottom: 2rem; }
                .cta-button { background: #ff6b6b; border: none; padding: 1rem 2rem; font-size: 1.1rem; margin: 0.5rem; }
                .features { padding: 3rem 0; }
                .feature-card { text-align: center; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 1rem 0; }
                .car-finder-widget { background: #f8f9fa; padding: 2rem; border-radius: 10px; margin: 2rem 0; }
                .pricing-card { border: 2px solid #e9ecef; border-radius: 10px; padding: 2rem; text-align: center; margin: 1rem 0; }
                .pricing-card.featured { border-color: #667eea; transform: scale(1.05); }
                .pricing-card h3 { color: #667eea; margin-bottom: 1rem; }
                .price { font-size: 2rem; font-weight: bold; color: #333; margin: 1rem 0; }
            """)
        ),
        Body(
            create_header(),
            
            # Hero Section
            Section(
                Container(
                    H1(NOVA_IDENTITY['name']),
                    P(NOVA_IDENTITY['tagline']),
                    P(NOVA_IDENTITY['mission']),
                    Div(
                        A("Find Your Perfect Car", href="/car-finder", cls="cta-button"),
                        A("View Our Services", href="/services", cls="cta-button", style="background: transparent; border: 2px solid white;")
                    )
                ),
                cls="hero"
            ),
            
            # AI Search Bar
            Section(
                Container(
                    Div(
                        H2("🤖 AI-Powered Car Search", style="text-align: center; margin-bottom: 2rem;"),
                        P("Just tell us what you need in plain English!", style="text-align: center; margin-bottom: 2rem;"),
                        Form(
                            Div(
                                Input(
                                    type="text", 
                                    name="ai_search", 
                                    placeholder="e.g., 'Luxury SUV for 7 people, hybrid, 3 days in Bangkok'",
                                    style="width: 100%; padding: 1rem; font-size: 1.1rem; border-radius: 8px; border: 2px solid #667eea;",
                                    required=True
                                ),
                                Button("🔍 Find My Perfect Car", type="submit", hx_post="/ai-search", hx_target="#ai-results", 
                                       style="width: 100%; margin-top: 1rem; background: #667eea; border: none; padding: 1rem; font-size: 1.1rem; border-radius: 8px; color: white;")
                            )
                        ),
                        Div(id="ai-results", style="margin-top: 2rem;")
                    ),
                    # Container already applies Main with cls="container"; avoid passing cls here to prevent conflict
                )
            ),
            
            # Traditional Car Finder Widget
            Section(
                Container(
                    Div(
                        H2("Or Use Our Traditional Car Finder"),
                        Form(
                            Div(
                                Label("How many passengers?"),
                                Select(
                                    Option("1-2 passengers", value="1-2"),
                                    Option("3-4 passengers", value="3-4"),
                                    Option("5-6 passengers", value="5-6"),
                                    Option("7+ passengers", value="7+"),
                                    name="passengers"
                                )
                            ),
                            Div(
                                Label("Car type preference:"),
                                Select(
                                    Option("Hatchback", value="hatchback"),
                                    Option("Sedan", value="sedan"),
                                    Option("SUV", value="suv"),
                                    Option("Van", value="van"),
                                    Option("Luxury", value="luxury"),
                                    name="car_type"
                                )
                            ),
                            Div(
                                Label("Energy type:"),
                                Select(
                                    Option("Electric", value="electric"),
                                    Option("Hybrid", value="hybrid"),
                                    Option("Fuel", value="fuel"),
                                    name="energy_type"
                                )
                            ),
                            Button("Find My Car", type="submit", hx_post="/car-match", hx_target="#car-results")
                        ),
                        Div(id="car-results"),
                        cls="car-finder-widget"
                    )
                )
            ),
            
            # Features Section
            Section(
                Container(
                    H2("Why Choose Nova?", style="text-align: center; margin-bottom: 3rem;"),
                    Div(
                        Div(
                            H3("🎯 Personalized Matching"),
                            P("Our AI-powered system finds the perfect car based on your specific needs and preferences."),
                            cls="feature-card"
                        ),
                        Div(
                            H3("💰 Best Pricing"),
                            P("Competitive rates with flexible rental periods from daily to yearly options."),
                            cls="feature-card"
                        ),
                        Div(
                            H3("🛡️ Complete Care"),
                            P("Full insurance coverage, maintenance programs, and 24/7 customer support."),
                            cls="feature-card"
                        ),
                        Div(
                            H3("🚀 Premium Service"),
                            P("Luxury vehicles, concierge service, and white-glove treatment for discerning customers."),
                            cls="feature-card"
                        ),
                        style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;"
                    )
                ),
                cls="features"
            ),
            
            # Pricing Preview
            Section(
                Container(
                    H2("Flexible Pricing Options", style="text-align: center; margin-bottom: 3rem;"),
                    Div(
                        Div(
                            H3("Basic"),
                            Div("$29/day", cls="price"),
                            Ul(
                                Li("Standard car selection"),
                                Li("Basic insurance coverage"),
                                Li("24/7 customer support")
                            ),
                            Button("Get Started", cls="secondary"),
                            cls="pricing-card"
                        ),
                        Div(
                            H3("Premium"),
                            Div("$49/day", cls="price"),
                            Ul(
                                Li("Premium car selection"),
                                Li("Full insurance coverage"),
                                Li("Priority customer support"),
                                Li("Free maintenance included")
                            ),
                            Button("Choose Premium", cls="primary"),
                            cls="pricing-card featured"
                        ),
                        Div(
                            H3("Luxury"),
                            Div("$89/day", cls="price"),
                            Ul(
                                Li("Luxury vehicle fleet"),
                                Li("Premium insurance coverage"),
                                Li("Concierge service"),
                                Li("All-inclusive maintenance")
                            ),
                            Button("Go Luxury", cls="secondary"),
                            cls="pricing-card"
                        ),
                        style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;"
                    )
                )
            ),
            
            create_footer()
        )
    )

@rt("/car-match", methods=["POST"])
def car_match(request: Request):
    form_data = request.form
    passengers = form_data.get("passengers", "")
    car_type = form_data.get("car_type", "")
    energy_type = form_data.get("energy_type", "")
    
    # Simple matching logic (in a real app, this would be more sophisticated)
    recommendations = []
    
    if car_type in CAR_CATEGORIES:
        cat_info = CAR_CATEGORIES[car_type]
        energy_info = ENERGY_TYPES.get(energy_type, {})
        
        recommendations.append({
            "name": f"{cat_info['name']} - {energy_info.get('name', 'Fuel')}",
            "icon": cat_info['icon'],
            "description": f"Perfect for {passengers}. {energy_info.get('description', '')}",
            "price": "$39/day" if car_type == "luxury" else "$29/day"
        })
    
    if not recommendations:
        recommendations.append({
            "name": "Popular Choice",
            "icon": "🚗",
            "description": "Based on your preferences, we recommend our most popular option.",
            "price": "$29/day"
        })
    
    return Div(
        H3("🎉 Perfect Matches for You!"),
        *[Div(
            H4(f"{rec['icon']} {rec['name']}"),
            P(rec['description']),
            P(f"Starting at {rec['price']}"),
            Button("Book This Car", cls="primary", style="margin-top: 1rem;")
        ) for rec in recommendations],
        Button("View All Options", href="/car-finder", cls="secondary", style="margin-top: 1rem;")
    )

@rt("/car-finder")
def car_finder():
    return Html(
        Head(
            Title("Car Finder - Nova"),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css")
        ),
        Body(
            create_header(),
            Main(
                H1("Find Your Perfect Car"),
                P("Answer a few questions and we'll match you with the ideal vehicle for your needs."),
                    
                    Form(
                        Div(
                            H3("1. How many passengers?"),
                            Div(
                                Input(type="radio", name="passengers", value="1-2", id="p1"),
                                Label("1-2 passengers", for_="p1")
                            ),
                            Div(
                                Input(type="radio", name="passengers", value="3-4", id="p2"),
                                Label("3-4 passengers", for_="p2")
                            ),
                            Div(
                                Input(type="radio", name="passengers", value="5-6", id="p3"),
                                Label("5-6 passengers", for_="p3")
                            ),
                            Div(
                                Input(type="radio", name="passengers", value="7+", id="p4"),
                                Label("7+ passengers", for_="p4")
                            )
                        ),
                        
                        Div(
                            H3("2. Car size/type preference:"),
                            Div(
                                Input(type="radio", name="car_type", value="hatchback", id="c1"),
                                Label("🚗 Hatchback - Compact & efficient", for_="c1")
                            ),
                            Div(
                                Input(type="radio", name="car_type", value="sedan", id="c2"),
                                Label("🚙 Sedan - Comfortable & stylish", for_="c2")
                            ),
                            Div(
                                Input(type="radio", name="car_type", value="suv", id="c3"),
                                Label("🚛 SUV - Spacious & versatile", for_="c3")
                            ),
                            Div(
                                Input(type="radio", name="car_type", value="van", id="c4"),
                                Label("🚐 Van - Maximum capacity", for_="c4")
                            ),
                            Div(
                                Input(type="radio", name="car_type", value="luxury", id="c5"),
                                Label("🏎️ Luxury - Premium experience", for_="c5")
                            )
                        ),
                        
                        Div(
                            H3("3. Travel purpose:"),
                            Div(
                                Input(type="radio", name="travel_purpose", value="daily", id="t1"),
                                Label("Daily commute", for_="t1")
                            ),
                            Div(
                                Input(type="radio", name="travel_purpose", value="weekend", id="t2"),
                                Label("Weekend trips", for_="t2")
                            ),
                            Div(
                                Input(type="radio", name="travel_purpose", value="long", id="t3"),
                                Label("Long distance travel", for_="t3")
                            ),
                            Div(
                                Input(type="radio", name="travel_purpose", value="cargo", id="t4"),
                                Label("Cargo transport", for_="t4")
                            )
                        ),
                        
                        Div(
                            H3("4. Style preference:"),
                            Div(
                                Input(type="radio", name="style", value="family", id="s1"),
                                Label("👨‍👩‍👧‍👦 Family-friendly", for_="s1")
                            ),
                            Div(
                                Input(type="radio", name="style", value="sport", id="s2"),
                                Label("🏁 Sport & performance", for_="s2")
                            ),
                            Div(
                                Input(type="radio", name="style", value="luxury", id="s3"),
                                Label("✨ Luxury & comfort", for_="s3")
                            ),
                            Div(
                                Input(type="radio", name="style", value="practical", id="s4"),
                                Label("🔧 Practical & reliable", for_="s4")
                            )
                        ),
                        
                        Div(
                            H3("5. Energy type preference:"),
                            Div(
                                Input(type="radio", name="energy", value="electric", id="e1"),
                                Label("⚡ Electric - Eco-friendly & efficient", for_="e1")
                            ),
                            Div(
                                Input(type="radio", name="energy", value="hybrid", id="e2"),
                                Label("🔄 Hybrid - Best of both worlds", for_="e2")
                            ),
                            Div(
                                Input(type="radio", name="energy", value="fuel", id="e3"),
                                Label("⛽ Traditional fuel - Proven reliability", for_="e3")
                            )
                        ),
                        
                        Button("Find My Perfect Car", type="submit", cls="primary", hx_post="/advanced-match", hx_target="#results")
                    ),
                    
                    Div(id="results", style="margin-top: 2rem;")
            ),
            create_footer()
        )
    )

@rt("/ai-search", methods=["POST"])
def ai_search(request: Request):
    """Handle AI-powered car search requests"""
    try:
        form_data = request.form
        user_input = form_data.get("ai_search", "")
        
        if not user_input:
            return Div("Please enter your car requirements.", style="color: red;")
        
        # Parse the user's natural language request
        parsed_request = parse_customer_request(user_input)
        
        # Generate AI recommendations
        recommendations = generate_ai_recommendations(parsed_request)
        
        # Generate chatbot response
        chatbot_response = generate_chatbot_response(parsed_request, recommendations)
    except Exception as e:
        print(f"AI search error: {e}")  # Debug output
        return Div(
            H3("🚨 Error Processing Request"),
            P("We encountered an issue processing your request. Please try again or use our traditional car finder."),
            P(f"Error details: {str(e)}"),
            Button("Use Traditional Finder", href="/car-finder", cls="secondary")
        )
    
    return Div(
        # Show parsed request
        Div(
            H3("🤖 I understood your request:"),
            Div(
                P(f"👥 Passengers: {parsed_request.get('passengers', 'Not specified')}"),
                P(f"🚗 Car Type: {parsed_request.get('car_type', 'Not specified').title()}"),
                P(f"⚡ Energy: {parsed_request.get('energy_type', 'Not specified').title()}"),
                P(f"🎨 Style: {parsed_request.get('style', 'Not specified').title()}"),
                P(f"📅 Duration: {parsed_request.get('duration', 'Not specified')} days"),
                P(f"📍 Location: {parsed_request.get('location', 'Not specified')}"),
                style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;"
            )
        ),
        
        # Show recommendations
        Div(
            H3("🎯 Your Perfect Matches"),
            *[Div(
                Div(
                    H4(f"{rec['image']} {rec['name']} - {rec['match_score']} Match"),
                    P(f"Model: {rec['model']} | Type: {rec['type']} | Energy: {rec['energy']} | Passengers: {rec['passengers']}"),
                    Div(f"Total: {rec['price']} ({rec['daily_price']})", style="font-size: 1.3rem; font-weight: bold; color: #667eea; margin: 0.5rem 0;"),
                    
                    # Features
                    Div(
                        H5("Features:"),
                        Ul(*[Li(feature) for feature in rec['features']])
                    ),
                    
                    # Insurance Options
                    Div(
                        H5("Insurance Options:"),
                        Ul(*[Li(option) for option in rec['insurance_options']])
                    ),
                    
                    # Add-ons
                    Div(
                        H5("Available Add-ons:"),
                        Ul(*[Li(addon) for addon in rec['add_ons']])
                    ),
                    
                    Div(
                        Button("Book This Car", cls="primary", 
                               hx_post=f"/checkout/{rec['id']}", 
                               hx_target="#checkout-modal"),
                        Button("Customize Options", cls="secondary", 
                               hx_post=f"/customize/{rec['id']}", 
                               hx_target="#customize-modal"),
                        style="margin-top: 1rem;"
                    ),
                    style="border: 2px solid #667eea; padding: 1.5rem; margin: 1rem 0; border-radius: 10px; background: white;"
                )
            ) for rec in recommendations]
        ),
        
        # Chatbot follow-up
        Div(
            H3("💬 Nova Assistant"),
            P(chatbot_response),
            Div(
                Button("Self-drive", cls="secondary", hx_post="/add-service/self-drive", hx_target="#service-added"),
                Button("Driver Service", cls="secondary", hx_post="/add-service/driver", hx_target="#service-added"),
                Button("Add Child Seats", cls="secondary", hx_post="/add-service/child-seats", hx_target="#service-added"),
                Button("Add GPS", cls="secondary", hx_post="/add-service/gps", hx_target="#service-added"),
                style="margin-top: 1rem;"
            ),
            style="background: #e3f2fd; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #2196f3;"
        ),
        
        Div(id="checkout-modal"),
        Div(id="customize-modal"),
        Div(id="service-added")
    )

@rt("/advanced-match", methods=["POST"])
def advanced_match(request: Request):
    form_data = request.form
    passengers = form_data.get("passengers", "")
    car_type = form_data.get("car_type", "")
    travel_purpose = form_data.get("travel_purpose", "")
    style = form_data.get("style", "")
    energy = form_data.get("energy", "")
    
    # Advanced matching logic
    recommendations = []
    
    # Generate recommendations based on selections
    if car_type == "hatchback":
        recommendations.append({
            "name": "Compact Eco Champion",
            "model": "Nova Eco",
            "type": "Hatchback",
            "energy": energy.title(),
            "price": "$25/day",
            "features": ["Perfect for city driving", "Low emissions", "Easy parking"],
            "match_score": "95%"
        })
    elif car_type == "suv":
        recommendations.append({
            "name": "Adventure Seeker",
            "model": "Nova Explorer",
            "type": "SUV",
            "energy": energy.title(),
            "price": "$45/day",
            "features": ["Spacious interior", "All-wheel drive", "Cargo space"],
            "match_score": "92%"
        })
    elif car_type == "luxury":
        recommendations.append({
            "name": "Luxury Experience",
            "model": "Nova Premium",
            "type": "Luxury",
            "energy": energy.title(),
            "price": "$89/day",
            "features": ["Premium amenities", "Concierge service", "White-glove treatment"],
            "match_score": "98%"
        })
    else:
        recommendations.append({
            "name": "Perfect Match",
            "model": "Nova Standard",
            "type": car_type.title(),
            "energy": energy.title(),
            "price": "$35/day",
            "features": ["Great value", "Reliable performance", "Popular choice"],
            "match_score": "88%"
        })
    
    return Div(
        H2("🎯 Your Perfect Matches"),
        P(f"Based on your preferences for {passengers} passengers, {car_type} type, {travel_purpose} travel, {style} style, and {energy} energy."),
        
        *[Div(
            H3(f"{rec['name']} - {rec['match_score']} Match"),
            P(f"Model: {rec['model']} | Type: {rec['type']} | Energy: {rec['energy']}"),
            Div(f"Starting at {rec['price']}", style="font-size: 1.5rem; font-weight: bold; color: #667eea;"),
            Ul(*[Li(feature) for feature in rec['features']]),
            Div(
                Button("Book This Car", cls="primary"),
                Button("View Details", cls="secondary"),
                style="margin-top: 1rem;"
            ),
            style="border: 1px solid #e9ecef; padding: 1.5rem; margin: 1rem 0; border-radius: 8px;"
        ) for rec in recommendations],
        
        Div(
            H3("Not finding what you're looking for?"),
            P("Our team can help you find the perfect car. Contact us for personalized assistance."),
            Button("Contact Nova Team", href="/contact", cls="secondary")
        )
    )

# Checkout and Upsell Routes
@rt("/checkout/<car_id>", methods=["POST"])
def checkout(car_id: str):
    """Show checkout modal with upsell opportunities"""
    return Div(
        Div(
            H3("🛒 Checkout - Nova Premium Elite"),
            P("You're booking: Nova Premium Elite (Luxury SUV)"),
            
            H4("Base Rental:"),
            P("$267 total for 3 days ($89/day)"),
            
            H4("Add-ons & Services:"),
            Div(
                Input(type="checkbox", name="insurance_premium", id="ins1"),
                Label("Premium Insurance (+$45 total)", for_="ins1"),
                style="margin: 0.5rem 0;"
            ),
            Div(
                Input(type="checkbox", name="driver_service", id="drv1"),
                Label("Personal Driver Service (+$150 total)", for_="drv1"),
                style="margin: 0.5rem 0;"
            ),
            Div(
                Input(type="checkbox", name="child_seats", id="child1"),
                Label("Child Seats (+$30 total)", for_="child1"),
                style="margin: 0.5rem 0;"
            ),
            Div(
                Input(type="checkbox", name="gps", id="gps1"),
                Label("GPS Navigation (+$15 total)", for_="gps1"),
                style="margin: 0.5rem 0;"
            ),
            
            H4("Cross-sell Opportunities:"),
            Div(
                Input(type="checkbox", name="maintenance_program", id="maint1"),
                Label("Nova Maintenance Program - 20% off first year", for_="maint1"),
                style="margin: 0.5rem 0; background: #fff3cd; padding: 0.5rem; border-radius: 4px;"
            ),
            Div(
                Input(type="checkbox", name="loyalty_membership", id="loyal1"),
                Label("Nova Premium Membership - Free upgrades on future rentals", for_="loyal1"),
                style="margin: 0.5rem 0; background: #d1ecf1; padding: 0.5rem; border-radius: 4px;"
            ),
            
            Div(
                P("Total: $267 + add-ons", style="font-size: 1.2rem; font-weight: bold; margin: 1rem 0;"),
                Button("Proceed to Payment", cls="primary", style="margin-right: 1rem;"),
                Button("Save for Later", cls="secondary")
            ),
            style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 500px; margin: 0 auto;"
        ),
        style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;"
    )

@rt("/add-service/<service_type>", methods=["POST"])
def add_service(service_type: str):
    """Add service to current booking"""
    service_names = {
        "self-drive": "Self-drive option selected",
        "driver": "Personal driver service added (+$50/day)",
        "child-seats": "Child seats added (+$10/day)",
        "gps": "GPS navigation added (+$5/day)"
    }
    
    return Div(
        P(f"✅ {service_names.get(service_type, 'Service added')}"),
        style="background: #d4edda; color: #155724; padding: 0.5rem; border-radius: 4px; margin: 0.5rem 0;"
    )

# Services Pages
@rt("/services")
def services():
    return Html(
        Head(
            Title("Services - Nova"),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"),
            Style("""
                .service-hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 3rem 0; text-align: center; }
                .service-card { border: 1px solid #e9ecef; border-radius: 10px; padding: 2rem; margin: 1rem 0; }
                .service-icon { font-size: 3rem; margin-bottom: 1rem; }
            """)
        ),
        Body(
            create_header(),
            
            Section(
                Container(
                    H1("Our Services"),
                    P("Comprehensive car solutions tailored to your needs")
                ),
                cls="service-hero"
            ),
            
            Main(
                Div(
                    Div(
                        Div("🚗", cls="service-icon"),
                            H3("Car Rental"),
                            P("Flexible rental options from daily to yearly contracts"),
                            Ul(
                                Li("Daily, weekly, monthly, and yearly rentals"),
                                Li("All car types and energy options"),
                                Li("Flexible pickup and return locations"),
                                Li("24/7 roadside assistance")
                            ),
                            Button("View Rental Options", href="/rental", cls="primary")
                        ),
                        cls="service-card"
                    ),
                    
                    Div(
                        Div(
                            Div("🛒", cls="service-icon"),
                            H3("Car Sales & Trade-in"),
                            P("Buy your perfect car or trade in your current vehicle"),
                            Ul(
                                Li("Extensive inventory of quality vehicles"),
                                Li("Fair trade-in evaluations"),
                                Li("Flexible financing options"),
                                Li("Warranty and after-sales support")
                            ),
                            Button("Browse Cars", href="/sales", cls="primary")
                        ),
                        cls="service-card"
                    ),
                    
                    Div(
                        Div(
                            Div("🔧", cls="service-icon"),
                            H3("Maintenance Programs"),
                            P("Keep your Nova vehicle in perfect condition"),
                            Ul(
                                Li("Regular maintenance scheduling"),
                                Li("Preventive care programs"),
                                Li("Emergency repair services"),
                                Li("Genuine parts and expert technicians")
                            ),
                            Button("Learn More", href="/maintenance", cls="primary")
                        ),
                        cls="service-card"
                    ),
                    
                    Div(
                        Div(
                            Div("🛡️", cls="service-icon"),
                            H3("Insurance Packages"),
                            P("Comprehensive coverage options for peace of mind"),
                            Ul(
                                Li("Basic, premium, and luxury coverage"),
                                Li("Competitive rates and quick claims"),
                                Li("24/7 customer support"),
                                Li("Flexible payment options")
                            ),
                            Button("Get Quote", href="/insurance", cls="primary")
                        ),
                        cls="service-card"
                    )
            ),
            
            create_footer()
        )
    )

@rt("/pricing")
def pricing():
    return Html(
        Head(
            Title("Pricing - Nova"),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"),
            Style("""
                .pricing-hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 3rem 0; text-align: center; }
                .pricing-card { border: 2px solid #e9ecef; border-radius: 15px; padding: 2rem; text-align: center; margin: 1rem; transition: transform 0.3s; }
                .pricing-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
                .pricing-card.featured { border-color: #667eea; transform: scale(1.05); background: #f8f9ff; }
                .price { font-size: 3rem; font-weight: bold; color: #667eea; margin: 1rem 0; }
                .features { text-align: left; margin: 1.5rem 0; }
            """)
        ),
        Body(
            create_header(),
            
            Section(
                Container(
                    H1("Simple, Transparent Pricing"),
                    P("Choose the plan that fits your needs and budget")
                ),
                cls="pricing-hero"
            ),
            
            Main(
                Div(
                    # Basic Tier
                        Div(
                            H3("Basic"),
                            Div("$29", cls="price"),
                            Small("/day", style="color: #666;"),
                            Div(
                                Ul(
                                    Li("Standard car selection"),
                                    Li("Basic insurance coverage"),
                                    Li("24/7 customer support"),
                                    Li("Standard maintenance"),
                                    Li("Flexible rental periods")
                                ),
                                cls="features"
                            ),
                            Button("Get Started", cls="secondary", style="width: 100%; margin-top: 1rem;")
                        ),
                        cls="pricing-card"
                    ),
                    
                    # Premium Tier (Featured)
                    Div(
                        H3("Premium"),
                        Small("Most Popular", style="background: #667eea; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem;"),
                        Div("$49", cls="price"),
                        Small("/day", style="color: #666;"),
                        Div(
                            Ul(
                                Li("Premium car selection"),
                                Li("Full insurance coverage"),
                                Li("Priority customer support"),
                                Li("Free maintenance included"),
                                Li("Concierge booking service"),
                                Li("Free delivery & pickup")
                            ),
                            cls="features"
                        ),
                        Button("Choose Premium", cls="primary", style="width: 100%; margin-top: 1rem;")
                    ),
                    cls="pricing-card featured"
                ),
                
                # Luxury Tier
                Div(
                    H3("Luxury"),
                    Div("$89", cls="price"),
                    Small("/day", style="color: #666;"),
                    Div(
                        Ul(
                            Li("Luxury vehicle fleet"),
                            Li("Premium insurance coverage"),
                            Li("Concierge service"),
                            Li("All-inclusive maintenance"),
                            Li("White-glove treatment"),
                            Li("Personal account manager")
                        ),
                        cls="features"
                    ),
                    Button("Go Luxury", cls="secondary", style="width: 100%; margin-top: 1rem;")
                ),
                cls="pricing-card"
            ),
            
            # Rental Period Options
            Section(
                Container(
                    H2("Flexible Rental Periods", style="text-align: center; margin: 3rem 0;"),
                    Div(
                        Div(
                            H4("Daily Rental"),
                            P("Perfect for short trips and weekend getaways"),
                            Ul(
                                Li("1-6 days: $29-89/day"),
                                Li("Same-day pickup available"),
                                Li("No long-term commitment")
                            )
                        ),
                        Div(
                            H4("Weekly Rental"),
                            P("Great for extended trips and business travel"),
                            Ul(
                                Li("7-29 days: $25-75/day"),
                                Li("10% discount on daily rates"),
                                Li("Free maintenance included")
                            )
                        ),
                        Div(
                            H4("Monthly Rental"),
                            P("Ideal for temporary vehicle needs"),
                            Ul(
                                Li("30+ days: $20-60/day"),
                                Li("20% discount on daily rates"),
                                Li("Priority vehicle selection")
                            )
                        ),
                        Div(
                            H4("Yearly Rental"),
                            P("Long-term solutions with maximum savings"),
                            Ul(
                                Li("365 days: $15-45/day"),
                                Li("30% discount on daily rates"),
                                Li("All-inclusive service")
                            )
                        ),
                        style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;"
                    )
            ),
            
            create_footer()
        )
    )

@rt("/contact")
def contact():
    return Html(
        Head(
            Title("Contact - Nova"),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"),
            Style("""
                .contact-hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 3rem 0; text-align: center; }
                .contact-card { background: #f8f9fa; padding: 2rem; border-radius: 10px; margin: 1rem 0; }
                .contact-info { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; }
            """)
        ),
        Body(
            create_header(),
            
            Section(
                Container(
                    H1("Get in Touch"),
                    P("We're here to help you find the perfect car solution")
                ),
                cls="contact-hero"
            ),
            
            Main(
                Div(
                    Div(
                        H3("Contact Information"),
                            Div(
                                P("📞 Phone: +1 (555) NOVA-CAR"),
                                P("✉️ Email: hello@nova-cars.com"),
                                P("📍 Address: 123 Auto Street, Car City, CC 12345"),
                                P("🕒 Hours: Mon-Fri 8AM-8PM, Sat-Sun 9AM-6PM")
                            ),
                            cls="contact-card"
                        ),
                        
                        Div(
                            H3("Send us a Message"),
                            Form(
                                Div(
                                    Input(type="text", name="name", placeholder="Your Name", required=True),
                                    Input(type="email", name="email", placeholder="Your Email", required=True)
                                ),
                                Div(
                                    Input(type="tel", name="phone", placeholder="Phone Number"),
                                    Select(
                                        Option("Select a service", value="", selected=True),
                                        Option("Car Rental", value="rental"),
                                        Option("Car Sales", value="sales"),
                                        Option("Maintenance", value="maintenance"),
                                        Option("Insurance", value="insurance"),
                                        Option("General Inquiry", value="general"),
                                        name="service"
                                    )
                                ),
                                Textarea(name="message", placeholder="Your message...", rows="5", required=True),
                                Button("Send Message", type="submit", cls="primary")
                            ),
                            cls="contact-card"
                        ),
                        
                        Div(
                            H3("Live Chat Support"),
                            P("Need immediate assistance? Chat with our team!"),
                            Button("Start Live Chat", cls="secondary", style="width: 100%;"),
                            P("Average response time: 2 minutes", style="font-size: 0.9rem; color: #666; margin-top: 1rem;"),
                            cls="contact-card"
                        ),
                        
                        cls="contact-info"
                    )
            ),
            
            create_footer()
        )
    )

@rt("/about")
def about():
    return Html(
        Head(
            Title("About Nova - Car Solutions"),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css")
        ),
        Body(
            create_header(),
            
            Main(
                H1("About Nova"),
                    H2("Our Vision"),
                    P(NOVA_IDENTITY['vision']),
                    
                    H2("Our Mission"),
                    P(NOVA_IDENTITY['mission']),
                    
                    H2("Why Choose Nova?"),
                    Ul(
                        Li("🎯 Personalized car matching based on your specific needs"),
                        Li("💰 Competitive pricing with flexible rental periods"),
                        Li("🛡️ Comprehensive insurance and maintenance programs"),
                        Li("🚀 Premium service for luxury vehicle experiences"),
                        Li("📱 Modern technology for seamless booking and management"),
                        Li("🌟 24/7 customer support and roadside assistance")
                    ),
                    
                    H2("Our Story"),
                    P("Nova was founded with a simple vision: to revolutionize the car rental and sales industry by putting the customer first. We believe that finding the perfect car should be easy, transparent, and tailored to your unique needs."),
                    
                    P("With years of experience in the automotive industry, our team has developed cutting-edge technology that matches you with the ideal vehicle based on your preferences, lifestyle, and budget. From eco-friendly electric vehicles to luxury cars, we have something for everyone."),
                    
                    H2("Our Values"),
                    Div(
                        Div(
                            H4("Customer First"),
                            P("Every decision we make is guided by what's best for our customers.")
                        ),
                        Div(
                            H4("Transparency"),
                            P("No hidden fees, no surprises. Clear pricing and honest communication.")
                        ),
                        Div(
                            H4("Innovation"),
                            P("We continuously improve our technology and services to serve you better.")
                        ),
                        Div(
                            H4("Sustainability"),
                            P("Committed to offering eco-friendly options and reducing environmental impact.")
                        ),
                        style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin: 2rem 0;"
                    )
            ),
            
            create_footer()
        )
    )

@rt("/ai-demo")
def ai_demo():
    """Demo page showcasing AI search functionality"""
    return Html(
        Head(
            Title("AI Search Demo - Nova"),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"),
            Style("""
                .demo-hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 3rem 0; text-align: center; }
                .demo-example { background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #667eea; }
                .demo-step { margin: 2rem 0; padding: 1.5rem; border: 1px solid #e9ecef; border-radius: 8px; }
                .demo-step h3 { color: #667eea; margin-bottom: 1rem; }
                .flow-arrow { text-align: center; font-size: 2rem; color: #667eea; margin: 1rem 0; }
            """)
        ),
        Body(
            create_header(),
            
            Section(
                Container(
                    H1("🤖 AI Search Demo"),
                    P("See how Nova's AI understands natural language and finds your perfect car")
                ),
                cls="demo-hero"
            ),
            
            Main(
                # Example 1
                    Div(
                        H2("Example 1: Luxury SUV Request"),
                        Div(
                            H3("👤 Customer Input:"),
                            P("Luxury SUV for 7 people, hybrid, 3 days in Bangkok", 
                              style="font-style: italic; background: #e3f2fd; padding: 1rem; border-radius: 4px;")
                        ),
                        Div(
                            H3("🤖 AI Parsing:"),
                            P("Passengers: 7 | Style: Luxury | Type: SUV | Energy: Hybrid | Duration: 3 days | Location: Bangkok")
                        ),
                        Div(
                            H3("🎯 AI Recommendations:"),
                            Ul(
                                Li("Nova Luxury Explorer - 98% Match - $267 total"),
                                Li("Nova Adventure - 92% Match - $135 total"),
                                Li("Nova Family Van - 95% Match - $165 total")
                            )
                        ),
                        Div(
                            H3("💬 AI Assistant Follow-up:"),
                            P("Great choices for 7 passengers! Would you like a driver service or self-drive? Also, do you need child seats or any cargo add-ons for your trip?")
                        ),
                        cls="demo-step"
                    ),
                    
                    Div("⬇️", cls="flow-arrow"),
                    
                    # Example 2
                    Div(
                        H2("Example 2: Family Trip Request"),
                        Div(
                            H3("👤 Customer Input:"),
                            P("Family car for weekend trip to beach, need space for kids", 
                              style="font-style: italic; background: #e3f2fd; padding: 1rem; border-radius: 4px;")
                        ),
                        Div(
                            H3("🤖 AI Parsing:"),
                            P("Passengers: 4 | Style: Family | Type: SUV | Energy: Fuel | Duration: 2 days | Location: Beach")
                        ),
                        Div(
                            H3("🎯 AI Recommendations:"),
                            Ul(
                                Li("Nova Family SUV - 95% Match - $90 total"),
                                Li("Nova Adventure - 92% Match - $90 total"),
                                Li("Nova Reliable - 88% Match - $70 total")
                            )
                        ),
                        Div(
                            H3("💬 AI Assistant Follow-up:"),
                            P("Perfect for your family beach trip! Would you like to add child seats, GPS navigation, or beach equipment storage?")
                        ),
                        cls="demo-step"
                    ),
                    
                    Div("⬇️", cls="flow-arrow"),
                    
                    # Example 3
                    Div(
                        H2("Example 3: Business Travel Request"),
                        Div(
                            H3("👤 Customer Input:"),
                            P("Professional car for business meetings, need to impress clients", 
                              style="font-style: italic; background: #e3f2fd; padding: 1rem; border-radius: 4px;")
                        ),
                        Div(
                            H3("🤖 AI Parsing:"),
                            P("Passengers: 2 | Style: Luxury | Type: Sedan | Energy: Fuel | Duration: 5 days | Location: Business district")
                        ),
                        Div(
                            H3("🎯 AI Recommendations:"),
                            Ul(
                                Li("Nova Premium Elite - 96% Match - $445 total"),
                                Li("Nova Business Class - 94% Match - $175 total"),
                                Li("Nova Reliable - 88% Match - $175 total")
                            )
                        ),
                        Div(
                            H3("💬 AI Assistant Follow-up:"),
                            P("Excellent choice for business meetings! Would you like our personal driver service, airport pickup, or luxury amenities to impress your clients?")
                        ),
                        cls="demo-step"
                    ),
                    
                    # Try it yourself
                    Div(
                        H2("🚀 Try It Yourself!"),
                        P("Test the AI search with your own natural language request:"),
                        Form(
                            Div(
                                Input(
                                    type="text", 
                                    name="demo_search", 
                                    placeholder="Describe your perfect car in plain English...",
                                    style="width: 100%; padding: 1rem; font-size: 1.1rem; border-radius: 8px; border: 2px solid #667eea;",
                                    required=True
                                ),
                                Button("🔍 Test AI Search", type="submit", hx_post="/ai-search", hx_target="#demo-results", 
                                       style="width: 100%; margin-top: 1rem; background: #667eea; border: none; padding: 1rem; font-size: 1.1rem; border-radius: 8px; color: white;")
                            )
                        ),
                        Div(id="demo-results", style="margin-top: 2rem;"),
                        cls="demo-step"
                    )
            ),
            
            create_footer()
        )
    )

# Debug route to test basic functionality
@rt("/test")
def test():
    """Simple test route to verify the app is working"""
    return Html(
        Head(Title("Test - Nova")),
        Body(
            H1("Nova Test Page"),
            P("If you can see this, the basic FastHTML setup is working!"),
            P("Testing AI configuration..."),
            Div(id="ai-test-result")
        )
    )

@rt("/test-ai")
def test_ai():
    """Test AI functionality"""
    try:
        # Test basic AI connection
        response = model.generate_content("Hello, are you working?")
        return Div(
            H3("✅ AI Test Successful!"),
            P(f"AI Response: {response.text[:100]}...")
        )
    except Exception as e:
        return Div(
            H3("❌ AI Test Failed"),
            P(f"Error: {str(e)}"),
            P("This might be due to API key issues or network connectivity.")
        )

if __name__ == "__main__":
    serve()
