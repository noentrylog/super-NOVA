# Nova Car Solutions Website

A comprehensive car solutions platform built with FastHTML, featuring AI-powered car matching, flexible rental options, and premium customer service.

## 🚗 About Nova

Nova is your trusted partner in finding the perfect car for you. We deliver the best, most personalized solutions to match every need through:

- **AI-Powered Matching**: Find your perfect car based on passenger count, car type, travel purpose, style preference, and energy type
- **Flexible Services**: Car rental (daily/weekly/monthly/yearly), sales, trade-ins, maintenance, and insurance
- **Transparent Pricing**: Three tiers (Basic $29/day, Premium $49/day, Luxury $89/day) with no hidden fees
- **Premium Service**: 24/7 support, concierge service, and white-glove treatment

## 🛠️ Technology Stack

- **Backend**: FastHTML (Python)
- **Frontend**: HTML5, CSS3, Pico CSS Framework
- **Interactivity**: HTMX for dynamic interactions
- **Styling**: Custom CSS with modern gradients and responsive design

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd super-NOVA
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and go to `http://localhost:5001`

## 📱 Features

### Core Functionality
- **Homepage**: Hero section with company branding and quick car finder
- **Car Finder**: Intelligent questionnaire to match customers with perfect vehicles
- **Services**: Comprehensive overview of rental, sales, maintenance, and insurance
- **Pricing**: Transparent tier structure with flexible rental periods
- **Contact**: Multiple contact methods including live chat integration
- **About**: Company story, values, and mission

### Interactive Elements
- **Car Matching**: Dynamic form with real-time recommendations
- **HTMX Integration**: Seamless page updates without full reloads
- **Responsive Design**: Mobile-first approach with modern UI/UX
- **Progressive Enhancement**: Works without JavaScript, enhanced with HTMX

### Customer Journey
1. **Discovery**: Landing page with value propositions
2. **Evaluation**: Car finder tool with personalized recommendations
3. **Decision**: Clear pricing and service options
4. **Booking**: Streamlined reservation process
5. **Service**: Premium delivery and ongoing support

## 🎯 Business Features

### Car Matching Algorithm
The system considers:
- **Passenger Count**: 1-2, 3-4, 5-6, 7+ passengers
- **Car Types**: Hatchback, Sedan, SUV, Van, Luxury
- **Travel Purpose**: Daily commute, weekend trips, long distance, cargo transport
- **Style Preference**: Family-friendly, sport, luxury, practical
- **Energy Type**: Electric, Hybrid, Traditional fuel

### Service Tiers
- **Basic ($29/day)**: Standard selection, basic insurance, 24/7 support
- **Premium ($49/day)**: Premium selection, full insurance, priority support, free maintenance
- **Luxury ($89/day)**: Luxury fleet, premium insurance, concierge service, white-glove treatment

### Rental Periods
- **Daily**: 1-6 days
- **Weekly**: 7-29 days (10% discount)
- **Monthly**: 30+ days (20% discount)
- **Yearly**: 365 days (30% discount)

## 🏗️ Project Structure

```
super-NOVA/
├── app.py                 # Main FastHTML application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── .dockerignore         # Docker ignore file
├── business-strategy.md  # Comprehensive business strategy
└── README.md            # This file
```

## 🐳 Docker Deployment

### Build and Run with Docker

1. Build the Docker image:
```bash
docker build -t nova-cars .
```

2. Run the container:
```bash
docker run -p 5001:5001 nova-cars
```

3. Access the application at `http://localhost:5001`

## 📊 Business Strategy

The project includes a comprehensive business strategy document (`business-strategy.md`) covering:

- **Customer Journey Workflows**: From inquiry to after-service
- **Marketing Copy**: Website content, slogans, social media posts
- **Upselling Strategies**: Insurance, maintenance, premium upgrades
- **Chatbot Flows**: Customer guidance and support
- **Pricing Strategy**: Tier structure and volume discounts
- **Risk Analysis**: Market, operational, and technology risks
- **Competitive Differentiation**: Unique value propositions

## 🎨 Design Philosophy

- **Modern & Clean**: Professional appearance with gradient backgrounds
- **User-Centric**: Intuitive navigation and clear information hierarchy
- **Mobile-First**: Responsive design that works on all devices
- **Accessibility**: Semantic HTML and proper contrast ratios
- **Performance**: Fast loading with optimized assets

## 🔧 Development

### Adding New Features
1. Define routes in `app.py` using `@rt("/path")` decorator
2. Create HTML components using FastHTML's element classes
3. Add styling in the `<Style>` section or external CSS
4. Implement HTMX for dynamic interactions

### Customization
- **Branding**: Update `NOVA_IDENTITY` dictionary for company information
- **Styling**: Modify CSS in the `<Style>` sections
- **Content**: Update text and copy throughout the application
- **Features**: Add new routes and functionality as needed

## 📈 Future Enhancements

- **Database Integration**: Store customer data and bookings
- **Payment Processing**: Integrated payment gateway
- **Real-time Chat**: Live customer support
- **Mobile App**: Native mobile application
- **AI Enhancement**: More sophisticated matching algorithms
- **Analytics**: Customer behavior tracking and insights

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Email: hello@nova-cars.com
- Phone: +1 (555) NOVA-CAR
- Website: https://nova-cars.com

---

**Nova Car Solutions** - Your Trusted Partner in Finding the Perfect Car 🚗✨
