from fasthtml.common import *
import json
from typing import Dict, List, Any

# Create FastHTML app
app, rt = fast_app()

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

def create_header():
    return Header(
        Nav(
            A("Nova", href="/", cls="brand"),
            Ul(
                Li(A("Find Your Car", href="/car-finder")),
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
            
            # Car Finder Widget
            Section(
                Container(
                    Div(
                        H2("Find Your Perfect Car in 3 Steps"),
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
                        Div(id="car-results")
                    ),
                    cls="car-finder-widget"
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
                Container(
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
                )
            ),
            create_footer()
        )
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
                    P("Comprehensive car solutions tailored to your needs"),
                    cls="service-hero"
                )
            ),
            
            Main(
                Container(
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
                    P("Choose the plan that fits your needs and budget"),
                    cls="pricing-hero"
                )
            ),
            
            Main(
                Container(
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
                    P("We're here to help you find the perfect car solution"),
                    cls="contact-hero"
                )
            ),
            
            Main(
                Container(
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
                Container(
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
                )
            ),
            
            create_footer()
        )
    )

if __name__ == "__main__":
    serve()
