# Decision Logic Tool Skill

## Description
An interactive decision-making tool for evaluating office space options based on multiple weighted criteria. Provides a comprehensive scoring system to help make data-driven real estate decisions.

## Capabilities
- Multi-criteria evaluation with weighted scoring
- Location assessment (0-10 scale)
- Building amenities evaluation
- Vicinity amenities evaluation
- Public transport accessibility rating
- Building size normalization
- Rental cost optimization (inverse scoring)
- Lease term flexibility assessment
- Detailed breakdown of weighted scores

## Evaluation Criteria

### 1. Location (Weight: 20%)
- Direct user input (0-10 scale)
- Considers proximity to business districts, accessibility, and strategic positioning

### 2. Building Amenities (Weight: 15%)
Individual amenities scored 0-10:
- End of Trip (EOT) facilities
- Wellness rooms
- Prayer rooms
- Meeting rooms
- Co-working spaces

### 3. Vicinity Amenities (Weight: 15%)
Individual amenities scored 0-10:
- Food & Beverage options
- Retail shops
- Gym facilities
- Banking services
- Childcare centers

### 4. Public Transport (Weight: 15%)
- Direct user input (0-10 scale)
- Considers proximity to MRT, bus stops, and transport hubs

### 5. Building Size (Weight: 10%)
- Input: Square footage
- Normalization: Assumes 20,000-35,000 sq ft range
- Formula: `min(10, building_size / 3000)`

### 6. Rental Cost (Weight: 15%)
- Input: Cost per square foot
- Inverse scoring (lower cost = higher score)
- Formula: `max(0, 10 - (rental_cost / 1.5))`
- Assumes $5-$15 per sq ft range

### 7. Lease Flexibility (Weight: 10%)
- Direct user input (0-10 scale)
- Considers lease term options and flexibility

## Scoring System
- **Raw Score**: Individual criterion score (0-10)
- **Weighted Score**: Raw score × weight × 10
- **Total Score**: Sum of all weighted scores (max 1000)

## Technical Implementation
- **Framework**: Flask
- **Route**: `/decisions`
- **Methods**: GET (form display), POST (calculation)
- **Template**: `templates/decisions.html`
- **Styling**: IBM Carbon Design System

## Usage
Access the tool at: `https://g8-app.azurewebsites.net/decisions`

## Input Form Structure
```
Location Score (0-10)
Transport Score (0-10)
Building Size (sq ft)
Rental Cost ($ per sq ft)
Lease Term Score (0-10)

Building Amenities (each 0-10):
- EOT Facilities
- Wellness Room
- Prayer Room
- Meeting Rooms
- Co-working Space

Vicinity Amenities (each 0-10):
- F&B Options
- Retail Shops
- Gym
- Bank
- Childcare
```

## Output
- **Total Score**: Aggregate weighted score
- **Breakdown Table**: 
  - Criteria name
  - Weight percentage
  - Raw score
  - Weighted score

## Use Cases
- Office relocation decisions
- Real estate portfolio evaluation
- Comparative analysis of multiple locations
- Stakeholder presentations with quantified metrics
- Budget vs amenities trade-off analysis

## Customization Options
- Adjust weights based on organizational priorities
- Modify normalization ranges for size and cost
- Add or remove amenity categories
- Change scoring scales

## Color Scheme
- Primary: IBM Carbon Design System
- Form styling: Clean, professional interface
- Results: Clear tabular presentation