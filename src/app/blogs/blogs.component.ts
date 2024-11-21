import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-blogs',
  templateUrl: './blogs.component.html',
  styleUrls: ['./blogs.component.css']
})
export class BlogsComponent implements OnInit {

  blogs = [
    {
      title: 'AI-Powered Notifications',
      description: 'Explore how AI is transforming the way notifications are managed and delivered to enhance user experience.',
      image: 'https://incubator.ucf.edu/wp-content/uploads/2023/07/artificial-intelligence-new-technology-science-futuristic-abstract-human-brain-ai-technology-cpu-central-processor-unit-chipset-big-data-machine-learning-cyber-mind-domination-generative-ai-scaled-1-1500x1000.jpg', 
      link: 'https://magenative.com/ai-powered-custom-push-notifications/'
    },
    {
      title: 'Blockchain in Tech Updates',
      description: 'Learn how blockchain is revolutionizing secure updates and notifications across decentralized systems.',
      image: 'https://blogs.iadb.org/caribbean-dev-trends/wp-content/uploads/sites/34/2017/12/Blockchain1.jpg', 
      link: 'https://blockchaintechnology-news.com/#:~:text=Blockchains%20could%20become%20the%20ultimate,almost%20instant%20payment%20authorisation...'
    },
    {
      title: 'Push Notifications Evolution',
      description: 'A deep dive into the evolution of push notifications and what the future holds for this technology.',
      image: 'https://clevertap.com/wp-content/uploads/2021/05/Push-Notification-Header.png', 
      link: 'https://www.ngrow.ai/blog/the-evolution-of-push-notifications-trends-shaping-user-engagement-in-2024'
    },
    {
      title: 'Cloud-Based Update Management',
      description: 'Discover the advantages of cloud-based systems in managing updates and delivering them seamlessly.',
      image: 'https://www.shutterstock.com/image-photo/man-use-laptop-cloud-computing-600nw-2018729366.jpg', 
      link: 'https://www.secopsolution.com/blog/windows-patch-management-in-the-cloud'
    },
    {
      title: 'IoT Updates and Notifications',
      description: 'Understand the role of the Internet of Things in delivering timely updates and notifications to devices.',
      image: 'https://images.prismic.io//intuzwebsite/078cae79-99e4-4114-80d7-c3beffd254c6_IoT+without+Internet-1.png?w=1200&q=80&auto=format,compress&fm=png8', 
      link: 'https://technanosoft.com/blog/iot-notifications#:~:text=A1%3A%20Notifying%20users%20or%20devices,Things%20devices%20in%20real%20time.'
    },
    {
      title: 'Data Security in Update Systems',
      description: 'An analysis of data security measures implemented in modern update and notification systems.',
      image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-tBleJgaFsmE3IJGo7qJepD7qOfVOkos5sgauW3_Hf-e7KWIVeFTe5sFGtkjVPAIumpU&usqp=CAU', 
      link: 'https://security.gallagher.com/en/Blog/Why-software-updates-are-important-for-security'
    },
    {
      title: 'Machine Learning for Predictive Updates',
      description: 'How machine learning is being used to predict necessary updates and automate notifications.',
      image: 'https://media.istockphoto.com/id/1319034403/photo/deep-learning.jpg?s=612x612&w=0&k=20&c=6e6C0087SmHq2CHHQ789DUi7xsihQS6bysokwFwpZ6A=', 
      link: 'https://www.valuecoders.com/blog/analytics/role-of-machine-learning-in-predictive-analytics-and-decision-making/#:~:text=Machine%20Learning%20models%20are%20then,that%20drive%20strategic%20decision%2Dmaking.'
    },
    {
      title: 'Cross-Platform Notifications',
      description: 'A look into cross-platform notification strategies for a consistent user experience.',
      image: 'https://miro.medium.com/v2/resize:fit:1400/1*BBOthbBs55UN8FaXsclx3g.png', 
      link: 'https://gravitec.net/blog/cross-platform-push-notifications-guide/'
    }
  ];

  constructor() { }

  ngOnInit(): void {
  }

  // goBack() {
  //   window.history.back(); 
  // }

}
