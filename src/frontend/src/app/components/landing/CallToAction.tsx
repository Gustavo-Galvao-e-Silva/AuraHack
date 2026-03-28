import { Link } from "react-router";
import { Button } from "../ui/button";
import { ArrowRight, Sparkles } from "lucide-react";
import { motion } from "motion/react";

const MotionDiv = motion.div;

export function CallToAction() {
    return(
      <section className="px-4 sm:px-6 lg:px-8 py-20 relative overflow-hidden">
        <div className="absolute inset-0 bg-linear-to-br from-primary/10 via-secondary/10 to-accent/10" />
        <MotionDiv
          className="max-w-4xl mx-auto text-center space-y-6 relative z-10"
          initial={{ scale: 0.9, opacity: 0 }}
          whileInView={{ scale: 1, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <motion.div
            animate={{ rotate: [0, 360] }}
            transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
            className="inline-block"
          >
            <Sparkles className="w-16 h-16 text-primary mb-4" />
          </motion.div>
          <h2 className="text-4xl sm:text-5xl font-bold text-foreground">
            Ready to Transform Clinical Research?
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Join the platform that's connecting patients to innovative treatments
            and helping researchers find qualified participants.
          </p>
          <Link to="/login">
            <Button size="lg" className="gap-2 shadow-2xl hover:scale-105 transition-transform">
              Create Free Account
              <ArrowRight className="w-5 h-5" />
            </Button>
          </Link>
        </MotionDiv>
      </section>
    );
}