# Self-Righting Boat

This project explores the optimized design of self-righting boats, including the development of mathematical models and software tools to support this endeavor.

---

## 📜 Context

Most ships lack the ability to self-right, making them vulnerable to capsizing under the influence of large waves and propulsion forces. Smaller and faster ships, in particular, are at higher risk.

While rescue boats and some sailing ships (equipped with heavy keels) are designed to self-right, other types of vessels, such as kiteboats, could benefit significantly from this capability. Kiteboats, subjected to strong pulling forces from kites, lack long, heavy keels and thus present unique design challenges.

This project aims to address these challenges and contribute to the safety and reliability of kiteboats and similar vessels.

---

## 🛠️ Installation

To install the required dependencies, follow the steps below:

1. Install `uv` by following the official [installation guide](https://docs.astral.sh/uv/getting-started/installation).
2. Alternatively, run the command from root of repository:  
   ```bash
   make install-uv
   ```

---

## 🚀 Usage

To launch an example, run the following command from root of repository:  
```bash
uv run hydrostatic_2d.py
```

## Test
   ```bash
   make test
   ```


---

## 📝 Features

- **Mathematical modeling:** Tools for analyzing hydrostatic and dynamic stability.
- **Software support:** Examples and scripts for evaluating boat designs.
- **Applications:** Tailored solutions for kiteboats and other vessels requiring self-righting capabilities.

---

## 🛠️ Development Roadmap

Features
- [x] Center of buoyancy computation
- [x] Vertical equilibrium
- [ ] Placement of center of gravity
- [ ] Righting arm (GZ) curve computation
- [ ] Research of equilibrium points
- [ ] Metacentric height computation at equilibrium points using flotation
- [ ] Optimized additional low density static superstructure to enable self-righting
- [ ] Optimized high density static keel to enable self-righting 

Geometry supported
- [ ] single 2D convex polygon
- [ ] multiple 2D convex polygons
- [ ] 2D convex polygons with closed holes (free surface effect)
- [ ] single 2D NURBS
- [ ] 3D meshes


## 📚 Credits

This project was initiated as part of the Ocean Options program at **École Centrale Nantes**. It was proposed by the **International Kiteboat Federation France (IKIFF)** [kiteboat.org], with the goal of improving the safety of kiteboats.

### Project Team:
- **Nicolas Fihey**  
- **Lucas Vieillefond**  
- **Thimothée Leroy**  
- Guidance by: **Baptiste Labat**

---

## 🤝 Contributions

Contributions are welcome! Please open an issue or submit a pull request to suggest changes, report bugs, or propose new features.

---

## 📜 License
![License](https://img.shields.io/badge/license-MPL%202.0-brightgreen)

This project is licensed under the Mozilla Public License 2.0 - see the [LICENSE](./LICENSE) file for details.

---

## 🖇️ References

- [International Kiteboat Federation France (IKIFF)](https://kiteboat.org)  
- (Include additional relevant references or resources)
