import { Component, NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WelcomeComponent } from './welcome/welcome.component';
import { LoginComponent } from './login/login.component';
// import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { SignupComponent } from './signup/signup.component';
import { TermsComponent } from './terms/terms.component';
import { HomeComponent } from './home/home.component';
import { AddTechnologyComponent } from './add-technology/add-technology.component'; 
import { TechnologiesComponent } from './technologies/technologies.component';
import { BlogsComponent } from './blogs/blogs.component';
import { SubscriptionComponent } from './subscriptions/subscriptions.component';
import { AboutComponent } from './about/about.component';
import { ContactComponent } from './contact/contact.component';
import { NotificationComponent } from './notification/notification.component';
import { UserDashboardComponent } from './user-dashboard/user-dashboard.component';
import { AdminHomeComponent } from './admin-home/admin-home.component';
import { AdminDashboardComponent } from './admin-dahboard/admin-dashboard.component';
import { AdminUsersComponent } from './admin-users/admin-users.component';
import { AdminTechComponent } from './admin-tech/admin-tech.component';
import { PreviousUpdatesComponent } from './previous-updates/previous-updates.component';
import { EarlierUpdatesComponent } from './earlier-updates/earlier-updates.component';
import { SearchedTermComponent } from './searched-term/searched-term.component';
import { ResetPasswordComponent } from './reset-password/reset-password.component';




const routes: Routes = [

  { path: '', component: WelcomeComponent},
  { path: 'login', component: LoginComponent },
  // { path: 'forgot-password', component: ForgotPasswordComponent },
  { path: 'reset-password' , component: ResetPasswordComponent},  
  { path: 'signup', component: SignupComponent },
  { path: 'search/:term', component: SearchedTermComponent},
  { path: 'home',component:HomeComponent},



  {path:'user',component:UserDashboardComponent,
    children:[
      { path: 'subscription', component: SubscriptionComponent},
      { path: 'technology', component: TechnologiesComponent},
      { path: 'blogs', component: BlogsComponent},
      { path: 'notification', component: NotificationComponent},
      { path: 'earlier-updates', component: EarlierUpdatesComponent},
      { path: 'previous-updates/:techId', component: PreviousUpdatesComponent},
      { path: 'home',component:HomeComponent},

      ]
  },

  {path:'admin', component:AdminDashboardComponent,
    children:[
      {path:'',component:AdminHomeComponent},
      { path: 'admin-users', component: AdminUsersComponent},
      { path: 'admin-tech', component: AdminTechComponent},
      { path: 'add-technology', component: AddTechnologyComponent },

    ]
  },

  { path: 'about-us', component: AboutComponent },
  { path: 'contact-us', component: ContactComponent},
  { path: 'terms', component: TermsComponent },
 
  { path: '**', redirectTo: '' },

 
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

