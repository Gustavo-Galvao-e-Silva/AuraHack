
import { Sparkles, Zap, Shield, Database, MessageSquare, TrendingUp } from "lucide-react";
import { motion } from "motion/react";

const MotionDiv = motion.div;

export function TechFeatures() {
    return(
      <section className="px-4 sm:px-6 lg:px-8 py-20">
        <div className="max-w-7xl mx-auto">
          <MotionDiv
            initial={{ y: 50, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl sm:text-5xl font-bold mb-4 text-foreground">
              Powered by Advanced Technology
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              State-of-the-art AI and machine learning to ensure the best matches
            </p>
          </MotionDiv>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { icon: Zap, title: "Lightning Fast", description: "Real-time matching with instant results" },
              { icon: Shield, title: "Secure & Private", description: "HIPAA compliant with end-to-end encryption" },
              { icon: Database, title: "Smart Vectorization", description: "AI-powered semantic analysis of medical data" },
              { icon: MessageSquare, title: "Direct Communication", description: "Built-in messaging system for seamless connection" },
              { icon: TrendingUp, title: "Match Scoring", description: "Percentage-based compatibility rating" },
              { icon: Sparkles, title: "Auto Updates", description: "Continuous updates from ClinicalTrials.gov" },
            ].map((feature, i) => (
              <MotionDiv
                key={i}
                initial={{ scale: 0.8, opacity: 0 }}
                whileInView={{ scale: 1, opacity: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                whileHover={{ scale: 1.05 }}
              >
                <div className="p-6 rounded-xl bg-linear-to-br from-card to-card/50 border border-border backdrop-blur-sm hover:shadow-lg transition-all duration-300">
                  <feature.icon className="w-10 h-10 text-primary mb-4" />
                  <h3 className="text-lg font-bold mb-2 text-foreground">{feature.title}</h3>
                  <p className="text-sm text-muted-foreground">{feature.description}</p>
                </div>
              </MotionDiv>
            ))}
          </div>
        </div>
      </section>
    );
}