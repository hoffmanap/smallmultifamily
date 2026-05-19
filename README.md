# Housing Affordability & Zoning Reform Toolkit

A collection of analysis tools, legislative tracking dashboards, and building code feasibility engines designed to streamline the development of middle-housing and multi-family projects.

## Project Summary

This project provides a comprehensive framework to support pro-housing policy reform. It bridges the gap between high-level legislative goals and ground-level development feasibility. By combining data-driven building code analysis with interactive planning tools, this toolkit helps planners, developers, and policymakers visualize the impact of regulatory changes on housing supply and cost.

## Tool Directory

### Building Code Value-Engineering Simulator
* **Purpose:** A calculator that visualizes the "regulatory cliff" between standard commercial codes and streamlined multi-family alternatives.
* **Function:** Compares baseline IBC requirements against proposed Title 18 amendments. It automatically adjusts interdependencies (sprinkler requirements, fire ratings, and egress) based on unit count, calculating the total capital savings realized by avoiding "over-regulation" of small-scale projects.

## Technical Stack
* **Language:** Python
* **Web Framework:** Streamlit (for dashboards and simulators)
* **Visualization:** PyDeck (for 3D massing/spatial rendering), Plotly (for financial indexing)
* **Data Handling:** Pandas (for structured CSV/Deed data)

## Getting Started

1. **Prerequisites:** Ensure you have Python installed.
2. **Setup:**
   ```bash
   pip install streamlit pandas plotly pydeck
